"""Экран ввода данных о тренировках."""

from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Input, Select
from textual.app import ComposeResult
from textual.widgets._select import NoSelection

from storage import add_workout
from messages import WorkoutSaved
from constants import (
    WORKOUT_TYPE_DISPLAY_NAMES,
    WORKOUT_DONE_YES,
    WORKOUT_DONE_NO,
    WorkoutType,
)


class EntryScreen(Screen):
    """Экран для ввода данных о тренировке."""

    BINDINGS = [
        ("s", "save", "Сохранить"),
        ("2", "go_stats", "Статистика"),
        ("q", "quit", "Выход"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Фиксация тренировки")
        yield Select(
            options=[
                (display_name, workout_type)
                for workout_type, display_name in WORKOUT_TYPE_DISPLAY_NAMES.items()
            ],
            id="type_select",
            prompt="Тип тренировки",
        )
        yield Select(
            options=[
                ("Была", WORKOUT_DONE_YES),
                ("Не была", WORKOUT_DONE_NO),
            ],
            id="was_done_select",
            prompt="Тренировка была?",
        )
        yield Input(
            placeholder="Комментарий к тренировке (необязательно)",
            id="comment_input",
            value="",
        )
        yield Button("Сохранить (S)", id="save_button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Обработчик нажатия на кнопку."""
        if event.button.id == "save_button":
            self.action_save()

    def _is_valid_selection(self, value: object) -> bool:
        """Проверяет, что значение Select не является NoSelection.
        
        Args:
            value: Значение из Select widget.
            
        Returns:
            bool: True если значение валидно, False если это NoSelection.
        """
        return not isinstance(value, NoSelection) and value is not None

    def action_save(self) -> None:
        """Сохраняет данные о тренировке."""
        type_select = self.query_one("#type_select", Select)
        was_done_select = self.query_one("#was_done_select", Select)
        comment_input = self.query_one("#comment_input", Input)

        # Проверки на пустые значения (NoSelection)
        if not self._is_valid_selection(type_select.value):
            self.app.notify("Выбери тип тренировки!", severity="error")
            return

        if not self._is_valid_selection(was_done_select.value):
            self.app.notify("Укажи статус тренировки!", severity="error")
            return

        # Преобразуем значения в нужные типы
        w_type: WorkoutType = type_select.value  # type: ignore[assignment]
        was_done = str(was_done_select.value) == WORKOUT_DONE_YES
        comment = comment_input.value.strip()

        add_workout(was_done=was_done, w_type=w_type, comment=comment)
        # Отправляем глобальный сигнал об обновлении
        self.app.post_message(WorkoutSaved())

        comment_input.value = ""
        self.app.notify("Тренировка сохранена!")

    def action_go_stats(self) -> None:
        """Переходит к экрану статистики."""
        self.app.push_screen("stats")

    def action_quit(self) -> None:
        """Выходит из приложения."""
        self.app.exit()
