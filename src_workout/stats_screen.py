"""Экран статистики тренировок."""

from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, DataTable
from textual.app import ComposeResult

from storage import get_stats, get_all_workouts, reset_data
from messages import WorkoutSaved
from constants import (
    WORKOUT_TYPE_DISPLAY_NAMES,
    WORKOUT_STATUS_DISPLAY_NAMES,
)


class StatsScreen(Screen):
    """Экран статистики тренировок."""

    BINDINGS = [
        ("1", "go_entry", "Ввод"),
        ("q", "quit", "Выход"),
        ("r", "reset_progress", "Сброс"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        # Таблица с деталями по дням
        self.table = DataTable(id="workouts_table")
        yield self.table
        
        # Итоги
        self.total_widget = Static(id="total")
        self.push_widget = Static(id="push_ups")
        self.strength_widget = Static(id="strength_set")
        yield self.total_widget
        yield self.push_widget
        yield self.strength_widget

        # Кнопка сброса
        yield Button("Сбросить прогресс (R)", id="reset_button", variant="primary")
        self.confirm_widget = Static("", id="confirm_text")
        yield self.confirm_widget

        yield Footer()

    def on_mount(self) -> None:
        """Инициализация экрана при монтировании."""
        # Настраиваем столбцы таблицы один раз
        self.table.add_columns("Дата", "Статус тренировки", "Тип тренировки", "Коммент")
        self.table.zebra_stripes = True
        self.table.cursor_type = "row"
        self.refresh_all()

    def refresh_all(self) -> None:
        """Обновляет и таблицу, и статистику."""
        self.refresh_table()
        self.refresh_stats()

    def refresh_table(self) -> None:
        """Обновляет таблицу с тренировками."""
        self.table.clear()
        workouts = get_all_workouts()
        workouts = sorted(workouts, key=lambda w: w.get("date", ""))

        for w in workouts:
            was_done = w.get("was_done", False)
            status = WORKOUT_STATUS_DISPLAY_NAMES.get(was_done, "Не была")
            workout_type = w.get("type", "")
            w_type = WORKOUT_TYPE_DISPLAY_NAMES.get(workout_type, workout_type)
            comment = w.get("comment", "")
            date_str = w.get("date", "")
            self.table.add_row(date_str, status, w_type, comment)

    def refresh_stats(self) -> None:
        """Обновляет виджеты статистики."""
        stats = get_stats()
        self.total_widget.update(f"Всего тренировок: {stats['total']}")
        self.push_widget.update(f"Push ups: {stats['push_ups']}")
        self.strength_widget.update(f"Strength set: {stats['strength_set']}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Обработчик нажатия на кнопку."""
        if event.button.id == "reset_button":
            self.action_reset_progress()

    def action_reset_progress(self) -> None:
        """Сбрасывает прогресс тренировок (требует подтверждения)."""
        # Простейший двухшаговый confirm
        if not getattr(self, "_awaiting_confirm", False):
            self._awaiting_confirm = True
            self.confirm_widget.update(
                "Точно сбросить весь прогресс? Нажми R ещё раз для подтверждения."
            )
            return
        # Пользователь подтвердил повторным нажатием R
        reset_data()
        self._awaiting_confirm = False
        self.confirm_widget.update("Прогресс сброшен.")
        self.refresh_all()  # Обновляем и таблицу, и статистику

    def action_go_entry(self) -> None:
        """Возвращается к экрану ввода."""
        self.app.pop_screen()

    def on_workout_saved(self, event: WorkoutSaved) -> None:
        """Обработчик события сохранения тренировки."""
        self.refresh_all()

    def action_quit(self) -> None:
        """Выходит из приложения."""
        self.app.exit()
