from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.widgets import Button, Static, Input, Label, Checkbox
from textual import on, work, events
from textual_fspicker import FileOpen, Filters
from tui.messages import MvrParsed, Errors
from tui.read_mvr import get_fixtures
from tui.merge_mvr import merger


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
            with Horizontal():
                yield Label("UI Single Line:")
                with Horizontal(id="details_checkbox_container"):
                    yield Checkbox(id="singleline_ui_toggle")
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
            self.query_one("#singleline_ui_toggle", Checkbox).value = self.data.get(
                "singleline_ui_toggle", True
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
                    "singleline_ui_toggle": self.query_one(
                        "#singleline_ui_toggle"
                    ).value,
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


class MVRScreen(ModalScreen):
    """Screen with a dialog to confirm quitting."""

    BINDINGS = [
        ("left", "focus_previous", "Focus Previous"),
        ("right", "focus_next", "Focus Next"),
        ("up", "focus_previous", "Focus Previous"),
        ("down", "focus_next", "Focus Next"),
    ]

    def compose(self) -> ComposeResult:
        with Grid(id="dialog"):
            yield Static("MVR Selection", id="question")

            with Horizontal(id="row1"):
                yield Button("Cancel", id="cancel")

            with Horizontal(id="row2"):
                yield Button("Import MVR", id="import_mvr")
                yield Button("Merge MVR files", id="merge_mvr")
                yield Button("Clean MVR data", id="clean_mvr")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "merge_mvr":
            self.dismiss()
            self.app.push_screen(MVRMergeScreen())

        if event.button.id == "clean_mvr":
            self.app.mvr_fixtures = []
            self.app.mvr_classes = []
            self.app.mvr_positions = []

            self.app.mvr_tag_display.update_items(
                self.app.mvr_positions
                + self.app.mvr_classes
                + [layer.layer for layer in self.app.mvr_fixtures]
            )

            self.app.mvr_fixtures_display.update_items(self.app.mvr_fixtures)
            self.app.query_one("#json_output").update("MVR data cleaned")
            self.app.query_one("#open_create_monitors").disabled = True
            self.dismiss()

        if event.button.id == "cancel":
            self.dismiss()

    @on(Button.Pressed)
    @work
    async def open_a_file(self, event: Button.Pressed) -> None:
        if event.button.id == "import_mvr":
            if opened := await self.app.push_screen_wait(
                FileOpen(filters=Filters(("MVR", lambda p: p.suffix.lower() == ".mvr")))
            ):
                try:
                    mvr_fixtures, mvr_tags = get_fixtures(opened)
                    self.post_message(MvrParsed(fixtures=mvr_fixtures, tags=mvr_tags))
                except Exception as e:
                    self.post_message(Errors(error=str(e)))

            self.dismiss()

    def action_focus_next(self) -> None:
        self.focus_next()

    def action_focus_previous(self) -> None:
        self.focus_previous()

    async def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.dismiss()  # Close the modal


class MVRMergeScreen(ModalScreen):
    """Screen with a dialog to confirm quitting."""

    file1 = None
    file2 = None
    BINDINGS = [
        ("left", "focus_previous", "Focus Previous"),
        ("right", "focus_next", "Focus Next"),
        ("up", "focus_previous", "Focus Previous"),
        ("down", "focus_next", "Focus Next"),
    ]

    def compose(self) -> ComposeResult:
        with Grid(id="dialog"):
            yield Static("Select MVR files for merging", id="question")

            with Horizontal(id="row1"):
                yield Button("Cancel", id="cancel")

            with Horizontal(id="row2"):
                yield Button("Select MVR file 1", id="file_button1")
                yield Button("Select MVR file 2 with IP addresses", id="file_button2")
            with Horizontal(id="row3"):
                yield Static("", id="file_name1")
                yield Static("", id="file_name2")

            with Horizontal(id="row4"):
                yield Button("Merge", id="do_merge", disabled=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "do_merge":
            if self.file1 and self.file2 and self.file1 != self.file2:
                try:
                    merger(self.file2, self.file1)
                    self.app.query_one("#json_output").update(
                        "Done! merged_with_network.mvr saved"
                    )
                except Exception as e:
                    self.post_message(Errors(error=str(e)))

            self.dismiss()

        if event.button.id == "cancel":
            self.dismiss()

    @on(Button.Pressed)
    @work
    async def open_a_file(self, event: Button.Pressed) -> None:
        if event.button.id == "file_button1":
            if opened := await self.app.push_screen_wait(
                FileOpen(filters=Filters(("MVR", lambda p: p.suffix.lower() == ".mvr")))
            ):
                self.file1 = opened
                self.check_files()

        if event.button.id == "file_button2":
            if opened := await self.app.push_screen_wait(
                FileOpen(filters=Filters(("MVR", lambda p: p.suffix.lower() == ".mvr")))
            ):
                self.file2 = opened
                self.check_files()

    def check_files(self):
        if self.file1:
            self.query_one("#file_name1").update(f"{self.file1.name}")
        if self.file2:
            self.query_one("#file_name2").update(f"{self.file2.name}")
        if self.file1 is not None and self.file2 and self.file1 != self.file2:
            self.query_one("#do_merge").disabled = False
        else:
            self.query_one("#do_merge").disabled = True

    def action_focus_next(self) -> None:
        self.focus_next()

    def action_focus_previous(self) -> None:
        self.focus_previous()

    async def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.dismiss()  # Close the modal
