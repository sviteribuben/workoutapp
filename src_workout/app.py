
from textual.app import App
from entry_screen import EntryScreen
from stats_screen import StatsScreen


class WorkoutApp(App):
    CSS_PATH = "app.tcss"

    def on_mount(self) -> None:
        self.install_screen(EntryScreen(), name="entry")
        self.install_screen(StatsScreen(), name="stats")
        self.push_screen("entry")


if __name__ == "__main__":
    WorkoutApp().run()
