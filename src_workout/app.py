"""Главный модуль приложения WorkoutApp."""

from textual.app import App

from entry_screen import EntryScreen
from stats_screen import StatsScreen


class WorkoutApp(App):
    """Главный класс приложения для отслеживания тренировок."""

    CSS_PATH = "app.tcss"

    def on_mount(self) -> None:
        """Инициализация приложения при запуске."""
        self.install_screen(EntryScreen(), name="entry")
        self.install_screen(StatsScreen(), name="stats")
        self.push_screen("entry")


if __name__ == "__main__":
    WorkoutApp().run()
