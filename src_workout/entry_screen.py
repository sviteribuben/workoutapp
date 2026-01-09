from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Input, Select
from textual.app import ComposeResult
from storage import add_workout


class EntryScreen(Screen):
    BINDINGS: list[tuple[str] | tuple[str, str, str]] = [
        ("s", "save", "Save workout"),
        ("2", "go_stats", "Go to stats"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Фиксация тренировки")
        # Select типа тренировки
        yield Select(
            options=[
                ("Push ups", "push_ups"),
                ("Strainge set", "straight_set"),
            ],
            id="type_select",
            prompt="Тип тренировки",
        )
        # Переключатель "была/не была" можно сделать как Input или Select
        yield Select(
            options=[("Была", "yes"), ("Не была", "no")],
            id="was_done_select",
            prompt="Тренировка была?",
        )
        # Поле комментария
        yield Input(
            placeholder="Комментарий к тренировке (необязательно)",
            id="comment_input",
        )
        yield Button("Сохранить (S)", id="save_button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_button":
            self.action_save()

    def action_save(self) -> None:
        type_select = self.query_one("#type_select", Select)
        was_done_select = self.query_one("#was_done_select", Select)
        comment_input = self.query_one("#comment_input", Input)

        w_type = type_select.value or "push_ups"
        was_done = (was_done_select.value == "yes")
        comment = comment_input.value.strip()

        add_workout(
            was_done=was_done, 
            w_type=w_type, comment=comment
            )

        # Очистить комментарий и показать уведомление
        comment_input.value = ""
        self.app.notify("Тренировка сохранена!")

    def action_go_stats(self) -> None:
        self.app.push_screen("stats")

    def action_quit(self) -> None:
        self.app.exit()
