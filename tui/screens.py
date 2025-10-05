from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal
from textual.widgets import Button, Static, Input, Label


class QuitScreen(ModalScreen[bool]):
    """Screen with a dialog to confirm quitting."""

    BINDINGS = [
        ("left", "focus_previous", "Focus Previous"),
        ("right", "focus_next", "Focus Next"),
        ("up", "focus_previous", "Focus Previous"),
        ("down", "focus_next", "Focus Next"),
    ]

    def compose(self) -> ComposeResult:
        yield Grid(
            Static("Are you sure you want to quit?", id="question"),
            Horizontal(
                Button("Yes", variant="error", id="yes"),
                Button("No", variant="primary", id="no"),
                id="buttons",
            ),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


class ConfigScreen(ModalScreen[dict]):
    """Screen with a dialog to configure URL, username and password."""

    BINDINGS = [
        ("left", "focus_previous", "Focus Previous"),
        ("right", "focus_next", "Focus Next"),
        ("up", "focus_previous", "Focus Previous"),
        ("down", "focus_next", "Focus Next"),
    ]

    def __init__(self, data: dict | None = None) -> None:
        self.data = data or {}
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("URL:"),
            Input(placeholder="Enter URL", id="url"),
            Label("Username:"),
            Input(placeholder="Enter username", id="username"),
            Label("Password:"),
            Input(placeholder="Enter password", id="password", password=True),
            Label("Timeout:"),
            Input(placeholder="Enter timeout (s)", id="timeout", type="integer"),
            Horizontal(
                Button("Save", variant="success", id="save"),
                Button("Cancel", variant="error", id="cancel"),
                id="config_buttons",
            ),
            id="config_dialog",
        )

    def on_mount(self) -> None:
        """Load existing data into the input fields."""
        if self.data:
            self.query_one("#url", Input).value = self.data.get("url", "")
            self.query_one("#username", Input).value = self.data.get("username", "")
            self.query_one("#password", Input).value = self.data.get("password", "")
            self.query_one("#timeout", Input).value = self.data.get("timeout", 1)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.dismiss(
                {
                    "url": self.query_one("#url").value,
                    "username": self.query_one("#username").value,
                    "password": self.query_one("#password").value,
                    "timeout": self.query_one("#timeout").value,
                }
            )
        else:
            self.dismiss({})
