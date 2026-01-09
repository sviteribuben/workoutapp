from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, DataTable
from textual.app import ComposeResult

from storage import get_stats, get_all_workouts, reset_data
from messages import WorkoutSaved


class StatsScreen(Screen):
    BINDINGS: list[tuple[str] | tuple[str, str, str]] = [
        ("1", "go_entry", "Go to entry"),
        ("q", "quit", "Quit"),
        ("r", "reset_progress", "Reset progress"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        # Таблица с деталями по дням
        self.table = DataTable(id="workouts_table")
        yield self.table
        
        # Итоги
        self.total_widget = Static(id="total")
        self.push_widget = Static(id="push_ups")
        self.straight_widget = Static(id="straight_set")
        yield self.total_widget
        yield self.push_widget
        yield self.straight_widget

        # Кнопка сброса
        yield Button("Сбросить прогресс (R)", id="reset_button", variant="primary")
        self.confirm_widget = Static("", id="confirm_text")
        yield self.confirm_widget

        yield Footer()

    def on_mount(self) -> None:
        # Настраиваем столбцы таблицы один раз
        self.table.add_columns("Дата", "Статус тренировки", "Тип тренировки", "Коммент")
        self.table.zebra_stripes = True
        self.table.cursor_type = "row"
        self.refresh_all()

    def refresh_all(self) -> None:
        self.refresh_table()
        self.refresh_stats()

    def refresh_table(self) -> None:
        self.table.clear()
        workouts = get_all_workouts()
        workouts = sorted(workouts, key=lambda w: w["date"])

        for w in workouts:
            status = "Была" if w["was_done"] else "Не была"
            if w["type"] == "push_ups":
                w_type = "Push ups"
            elif w["type"] == "straight_set":
                w_type = "Strainge set"
            else:
                w_type = w["type"]
            comment = w.get("comment", "")
            self.table.add_row(w["date"], status, w_type, comment)

    def refresh_stats(self) -> None:
        stats = get_stats()
        self.total_widget.update(f"Всего тренировок: {stats['total']}")
        self.push_widget.update(f"Push ups: {stats['push_ups']}")
        self.straight_widget.update(f"Strainge set: {stats['straight_set']}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "reset_button":
            self.action_reset_progress()

    def action_reset_progress(self) -> None:
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
        self.refresh_stats()

    def action_go_entry(self) -> None:
        self.app.pop_screen()  # или self.app.switch_screen("entry")

    def on_workout_saved(self, event: WorkoutSaved) -> None:
        self.refresh_all()

    def action_quit(self) -> None:
        self.app.exit()
