from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.widgets import Button, Static, Input, Label, Checkbox
from textual import events


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

    def action_focus_next(self) -> None:
        self.focus_next()

    def action_focus_previous(self) -> None:
        self.focus_previous()

    async def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.dismiss()  # Close the modal


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
        with Vertical(id="config_dialog"):
            yield Static("Settings", id="config_question")
            with Horizontal():
                yield Label("Uptime Kuma Server URL:")
                yield Input(placeholder="Enter URL", id="url")
            with Horizontal():
                yield Label("Username:")
                yield Input(placeholder="Enter username", id="username")
            with Horizontal():
                yield Label("Password:")
                yield Input(placeholder="Enter password", id="password", password=True)
            with Horizontal():
                yield Label("API Network Timeout:")
                yield Input(
                    placeholder="Enter timeout (s)", id="timeout", type="integer"
                )
            with Horizontal():
                yield Label("Show IDs in listing:")
                with Horizontal(id="details_checkbox_container"):
                    yield Checkbox(id="details_toggle")
            yield Horizontal(
                Button("Save", variant="success", id="save"),
                Button("Cancel", variant="error", id="cancel"),
                id="config_buttons",
            )

    def on_mount(self) -> None:
        """Load existing data into the input fields."""
        if self.data:
            self.query_one("#url", Input).value = self.data.get("url", "")
            self.query_one("#username", Input).value = self.data.get("username", "")
            self.query_one("#password", Input).value = self.data.get("password", "")
            self.query_one("#timeout", Input).value = self.data.get("timeout", "1")
            self.query_one("#details_toggle", Checkbox).value = self.data.get(
                "details_toggle", False
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.dismiss(
                {
                    "url": self.query_one("#url").value,
                    "username": self.query_one("#username").value,
                    "password": self.query_one("#password").value,
                    "timeout": self.query_one("#timeout").value,
                    "details_toggle": self.query_one("#details_toggle").value,
                }
            )
        else:
            self.dismiss({})

    def action_focus_next(self) -> None:
        self.focus_next()

    def action_focus_previous(self) -> None:
        self.focus_previous()

    async def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.dismiss()  # Close the modal


class DeleteScreen(ModalScreen):
    """Screen with a dialog to confirm quitting."""

    BINDINGS = [
        ("left", "focus_previous", "Focus Previous"),
        ("right", "focus_next", "Focus Next"),
        ("up", "focus_previous", "Focus Previous"),
        ("down", "focus_next", "Focus Next"),
    ]

    def compose(self) -> ComposeResult:
        with Grid(id="dialog"):
            yield Static("This will delete data from Uptime Kuma!", id="question")

            with Horizontal(id="row1"):
                yield Button("Cancel", id="cancel")

            with Horizontal(id="row2"):
                yield Button("Delete All Monitors", id="delete_monitors")
                yield Button("Delete All Tags", id="delete_tags")

            with Horizontal(id="row3"):
                yield Button("Delete Loaded MVR Monitors", id="delete_mvr_monitors")
                yield Button("Delete Loaded MVR Tags", id="delete_mvr_tags")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete_monitors":
            self.app.run_api_get_data()
            self.app.run_api_delete_monitors()
            self.app.disable_buttons()
            self.dismiss()

        if event.button.id == "delete_tags":
            self.app.run_api_get_data()
            self.app.run_api_delete_tags()
            self.app.disable_buttons()
            self.dismiss()

        if event.button.id == "delete_mvr_monitors":
            self.app.run_api_get_data()
            self.app.run_api_delete_monitors(mvr=True)
            self.app.disable_buttons()
            self.dismiss()

        if event.button.id == "delete_mvr_tags":
            self.app.run_api_get_data()
            self.app.run_api_delete_tags(mvr=True)
            self.app.disable_buttons()
            self.dismiss()
        if event.button.id == "cancel":
            self.dismiss()

    def action_focus_next(self) -> None:
        self.focus_next()

    def action_focus_previous(self) -> None:
        self.focus_previous()

    async def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.dismiss()  # Close the modal


class AddMonitorsScreen(ModalScreen[dict]):
    """Screen with a dialog to confirm quitting."""

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
            Static("Add Monitors", id="question"),
            Horizontal(
                Button("Add Monitors", id="create_monitors"),
                Button("Cancel", id="cancel"),
                id="row2",
            ),
            Vertical(
                Static("Create Tags From:"),
                Horizontal(
                    Checkbox("Layers", id="layers_toggle"),
                    Checkbox("Classes", id="classes_toggle"),
                    Checkbox("Positions", id="positions_toggle"),
                    id="behavior_options",
                ),
                id="checkbox_container",
            ),
            id="dialog",
        )

    def on_mount(self) -> None:
        self.query_one("#layers_toggle").value = self.data.get("layers", False)
        self.query_one("#classes_toggle").value = self.data.get("classes", False)
        self.query_one("#positions_toggle").value = self.data.get("positions", False)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        data = {
            "layers": self.query_one("#layers_toggle").value,
            "classes": self.query_one("#classes_toggle").value,
            "positions": self.query_one("#positions_toggle").value,
        }
        if event.button.id == "create_monitors":
            self.app.query_one("#json_output").update(
                "Calling API via script, adding monitors..."
            )
            self.app.run_api_create_monitors(data)
            self.app.disable_buttons()
            self.dismiss(data)  # Close the modal

        if event.button.id == "cancel":
            self.dismiss(data)  # Close the modal

    def action_focus_next(self) -> None:
        self.focus_next()

    def action_focus_previous(self) -> None:
        self.focus_previous()

    async def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            data = {
                "layers": self.query_one("#layers_toggle").value,
                "classes": self.query_one("#classes_toggle").value,
                "positions": self.query_one("#positions_toggle").value,
            }
            self.dismiss(data)  # Close the modal
