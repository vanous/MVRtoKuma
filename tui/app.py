import functools
import json
import os
import random
import traceback
import subprocess
from types import SimpleNamespace
from textual.app import App, ComposeResult
from textual import on, work
from textual.containers import Horizontal, Vertical, VerticalScroll, Grid
from textual.widgets import Header, Footer, Input, Button, Checkbox, Static
from textual.worker import Worker, WorkerState
from tui.screens import QuitScreen, ConfigScreen, DeleteScreen
from uptime_kuma_api import UptimeKumaApi, MonitorType, UptimeKumaException
from textual.message import Message
from tui.fixture import KumaFixture, KumaTag
from textual_fspicker import FileOpen, Filters
from tui.read_mvr import get_fixtures
from textual.reactive import reactive


class ListDisplay(Vertical):
    def update_items(self, items: list):
        self.remove_children()
        for item in items:
            tags = ""
            if hasattr(item, "tags"):
                tags = item.tags
            self.mount(Static(f"{item.name} {item.uuid or ''} {item.id or ''} {tags}"))


class DictListDisplay(Vertical):
    def update_items(self, items: list):
        self.remove_children()
        for item in items:  # layers
            for fixture in item["fixtures"]:
                self.mount(Static(f"{fixture.name} {fixture.uuid}"))


class MonitorsFetched(Message):
    """Message sent when monitors are fetched from the API."""

    def __init__(self, monitors: list | None = None) -> None:
        self.monitors = monitors
        super().__init__()


class MvrParsed(Message):
    """Message sent when monitors are fetched from the API."""

    def __init__(self, fixtures: list | None = None, tags: list | None = None) -> None:
        self.fixtures = fixtures
        self.tags = tags
        super().__init__()


class TagsFetched(Message):
    """Message sent when monitors are fetched from the API."""

    def __init__(self, tags: list | None = None, error: str | None = None) -> None:
        self.tags = tags
        super().__init__()


class Errors(Message):
    """Message sent when monitors are fetched from the API."""

    def __init__(self, error: str | None = None) -> None:
        self.error = error
        super().__init__()


class UptimeKumaMVR(App):
    """A Textual app to manage Uptime Kuma MVR."""

    CSS_PATH = ["app.css", "quit_screen.css", "config_screen.css", "delete_screen.css"]
    BINDINGS = [
        ("left", "focus_previous", "Focus Previous"),
        ("right", "focus_next", "Focus Next"),
        ("up", "focus_previous", "Focus Previous"),
        ("down", "focus_next", "Focus Next"),
    ]
    HORIZONTAL_BREAKPOINTS = [
        (0, "-narrow"),
        (40, "-normal"),
        (80, "-wide"),
        (120, "-very-wide"),
    ]

    CONFIG_FILE = "config.json"
    url: str = ""
    username: str = ""
    password: str = ""
    timeout: str = ""

    kuma_fixtures = []
    kuma_tags = []
    mvr_fixtures = []
    mvr_tags = []

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        with Vertical():
            with VerticalScroll(id="json_output_container"):
                yield Static("No Errors...", id="json_output")
                with Horizontal():
                    with Vertical(id="left"):
                        yield Static("[b]MVR data:[/b]")
                        self.mvr_tag_display = ListDisplay()
                        yield self.mvr_tag_display
                        self.mvr_fixtures_display = DictListDisplay()
                        yield self.mvr_fixtures_display
                    with Vertical(id="right"):
                        yield Static("[b]Uptime Kuma data:[/b]")
                        self.kuma_tag_display = ListDisplay()
                        yield self.kuma_tag_display
                        self.kuma_fixtures_display = ListDisplay()
                        yield self.kuma_fixtures_display

            with Grid(id="action_buttons"):
                yield Button("Get Server Data", id="get_button")
                yield Button("Import MVR", id="import_button")
                yield Button("Add Tags", id="create_tags")
                yield Button("Add Monitors", id="create_monitors")
                yield Button("Delete", id="delete_screen")
                yield Button("Configure", id="configure_button")
                yield Button("Quit", variant="error", id="quit")
            with Vertical(id="checkbox_container"):
                yield Static("Use for Tags:")
                with Horizontal(id="behavior_options"):
                    yield Checkbox("Layers ", id="layers_toggle")
                    # yield Checkbox("Groups ", id="groups_toggle")
                    yield Checkbox("Classes ", id="classes_toggle")

    def on_mount(self) -> None:
        """Load the configuration from the JSON file when the app starts."""
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as f:
                try:
                    data = json.load(f)
                    self.url = data.get("url", "")
                    self.username = data.get("username", "")
                    self.password = data.get("password", "")
                    self.timeout = data.get("timeout", "1")
                    self.query_one("#layers_toggle").value = data.get("layers", False)
                    # self.query_one("#groups_toggle").value = data.get("groups", False)
                    self.query_one("#classes_toggle").value = data.get("classes", False)
                except json.JSONDecodeError:
                    # Handle empty or invalid JSON file
                    pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        if event.button.id == "create_tags":
            self.query_one("#json_output").update(
                "Calling API via script, adding tags..."
            )
            self.run_api_create_tags()
            self.run_api_get_data()

        if event.button.id == "create_monitors":
            self.query_one("#json_output").update(
                "Calling API via script, adding monitors..."
            )
            self.run_api_create_monitors()
            self.run_api_get_data()

        if event.button.id == "delete_screen":
            self.push_screen(DeleteScreen())

        if event.button.id == "delete_tags":
            self.query_one("#json_output").update(
                "Calling API via script, adding monitors..."
            )
            self.run_api_delete_tags()
            self.run_api_get_data()

        if event.button.id == "get_button":
            self.query_one("#json_output").update("Calling API via script...")
            # self.query_one("#get_button").disabled = True
            self.run_api_get_data()
            # worker_callable = functools.partial(self.run_api_script_worker, url)
            # self.run_worker(worker_callable, thread=True)

        if event.button.id == "configure_button":
            current_config = {
                "url": self.url,
                "username": self.username,
                "password": self.password,
                "timeout": self.timeout,
            }

            def save_config(data: dict) -> None:
                """Called with the result of the configuration dialog."""
                if data:
                    self.url = data.get("url", "")
                    self.username = data.get("username", "")
                    self.password = data.get("password", "")
                    self.timeout = data.get("timeout", "1")
                    self.action_save_config()
                    self.notify("Configuration saved.")

            self.push_screen(ConfigScreen(data=current_config), save_config)

        if event.button.id == "quit":

            def check_quit(quit_confirmed: bool) -> None:
                """Called with the result of the quit dialog."""
                if quit_confirmed:
                    self.action_quit()

            self.push_screen(QuitScreen(), check_quit)

    @on(Button.Pressed)
    @work
    async def open_a_file(self, event: Button.Pressed) -> None:
        if event.button.id == "import_button":
            if opened := await self.push_screen_wait(
                FileOpen(filters=Filters(("MVR", lambda p: p.suffix.lower() == ".mvr")))
            ):
                try:
                    mvr_fixtures, mvr_tags = get_fixtures(opened)
                    self.post_message(MvrParsed(fixtures=mvr_fixtures, tags=mvr_tags))
                except Exception as e:
                    self.post_message(Errors(error=str(e)))

    def on_monitors_fetched(self, message: MonitorsFetched) -> None:
        # output_widget = self.query_one("#json_output", Static)
        # self.query_one("#get_button", Button).disabled = False

        # formatted = json.dumps(message.monitors, indent=2)
        # output_widget.update(f"[green]Monitors Fetched:[/green]\n{formatted}")
        self.kuma_fixtures = [KumaFixture(f) for f in message.monitors]
        # for fixture in self.kuma_fixtures:
        #    print(fixture)

        self.kuma_fixtures_display.update_items(self.kuma_fixtures)

    def on_tags_fetched(self, message: MonitorsFetched) -> None:
        # output_widget = self.query_one("#json_output", Static)
        # self.query_one("#get_button", Button).disabled = False

        # formatted = json.dumps(message.tags, indent=2)
        # output_widget.update(f"[green]Tags Fetched:[/green]\n{formatted}")
        self.kuma_tags = [KumaTag(t) for t in message.tags]
        # for tag in self.kuma_tags:
        #    print(tag)

        self.kuma_tag_display.update_items(self.kuma_tags)

    def on_mvr_parsed(self, message: MvrParsed) -> None:
        # output_widget = self.query_one("#json_output", Static)
        # self.query_one("#get_button", Button).disabled = False

        self.mvr_fixtures = message.fixtures
        self.mvr_tags += message.tags["layers"]
        self.mvr_tags += message.tags["classes"]

        self.mvr_tag_display.update_items(self.mvr_tags)
        self.mvr_fixtures_display.update_items(self.mvr_fixtures)

    def on_errors(self, message: Errors) -> None:
        output_widget = self.query_one("#json_output", Static)
        # self.query_one("#get_button", Button).disabled = False

        if message.error:
            output_widget.update(f"[red]Error:[/red] {message.error}")

    @work(exclusive=True)
    async def run_api_get_data(self) -> str:
        # Safe to call blocking code here
        api = None
        try:
            api = UptimeKumaApi(self.url, timeout=int(self.timeout))
            api.login(self.username, self.password)
        except Exception as e:
            self.post_message(Errors(error=str(e)))

        if not api:
            self.post_message(Errors(error="Not logged in"))
            return
        try:
            monitors = api.get_monitors()
            # You can now emit a message or update reactive variables
            self.post_message(MonitorsFetched(monitors=monitors))
        except Exception as e:
            self.post_message(Errors(error=str(e)))

        try:
            print("get tags")
            tags = api.get_tags()
            print("get tags", tags)
            # You can now emit a message or update reactive variables
            self.post_message(TagsFetched(tags=tags))
        except Exception as e:
            self.post_message(Errors(error=str(e)))

    @work(exclusive=True)
    async def run_api_delete_tags(self) -> str:
        # Safe to call blocking code here
        api = None
        try:
            api = UptimeKumaApi(self.url, timeout=int(self.timeout))
            api.login(self.username, self.password)
        except Exception as e:
            traceback.print_exception(e)
            self.post_message(Errors(error=str(e)))

        if not api:
            self.post_message(Errors(error="Not logged in"))
            return
        try:
            for tag in self.kuma_tags:
                api.delete_tag(tag.id)

        except Exception as e:
            traceback.print_exception(e)
            self.post_message(Errors(error=str(e)))

    @work(exclusive=True)
    async def run_api_delete_monitors(self) -> str:
        # Safe to call blocking code here
        api = None
        try:
            api = UptimeKumaApi(self.url, timeout=int(self.timeout))
            api.login(self.username, self.password)
        except Exception as e:
            traceback.print_exception(e)
            self.post_message(Errors(error=str(e)))

        if not api:
            self.post_message(Errors(error="Not logged in"))
            return
        try:
            for monitor in self.kuma_fixtures:
                api.delete_monitor(monitor.id)

        except Exception as e:
            traceback.print_exception(e)
            self.post_message(Errors(error=str(e)))

    @work(exclusive=True)
    async def run_api_create_monitors(self) -> str:
        # Safe to call blocking code here
        api = None
        try:
            api = UptimeKumaApi(self.url, timeout=int(self.timeout))
            api.login(self.username, self.password)
        except Exception as e:
            traceback.print_exception(e)
            self.post_message(Errors(error=str(e)))

        if not api:
            self.post_message(Errors(error="Not logged in"))
            return
        try:
            for layer in self.mvr_fixtures:
                print("debug layer", layer)

                for mvr_fixture in layer.get("fixtures", []):
                    url = None
                    for network in mvr_fixture.addresses.network:
                        if network.ipv4 is not None:
                            url = network.ipv4
                            break
                    if url is None:
                        continue

                    monitor_id = None
                    monitor_tags = []
                    add_monitor = True
                    add_tag = None
                    for kuma_fixture in self.kuma_fixtures:
                        # print(f"{kuma_fixture.name=} {mvr_fixture=}")
                        if mvr_fixture.uuid == kuma_fixture.uuid:
                            add_monitor = False
                            monitor_id = kuma_fixture.id
                            monitor_tags = kuma_fixture.tags
                            print("Monitor already exists", monitor_id, monitor_tags)
                            break
                    if add_monitor:
                        print("Add new monitor")
                        result = api.add_monitor(
                            type=MonitorType.HTTP,
                            name=mvr_fixture.name,
                            url=f"http://{url}",
                            description=mvr_fixture.uuid,
                        )

                        monitor_id = result.get("monitorID", None)
                    if monitor_id is not None:
                        if self.query_one("#layers_toggle").value:
                            for kuma_tag in self.kuma_tags:
                                if kuma_tag.name == layer["layer"].name:
                                    if kuma_tag.name not in monitor_tags:
                                        print(
                                            f"{monitor_id=}, {kuma_tag.id=}, {kuma_tag.name=}, {monitor_tags=}"
                                        )
                                        add_tag = kuma_tag.id
                            if add_tag:
                                try:
                                    api.add_monitor_tag(
                                        monitor_id=monitor_id,
                                        tag_id=kuma_tag.id,
                                    )
                                except Exception as e:
                                    print(e)

        except Exception as e:
            traceback.print_exception(e)
            self.post_message(Errors(error=str(e)))

    @work(exclusive=True)
    async def run_api_create_tags(self) -> str:
        # Safe to call blocking code here
        api = None
        try:
            api = UptimeKumaApi(self.url, timeout=int(self.timeout))
            api.login(self.username, self.password)
        except Exception as e:
            self.post_message(Errors(error=str(e)))

        if not api:
            self.post_message(Errors(error="Not logged in"))
            return
        try:
            for tag in self.mvr_tags:
                add = True
                for kuma_tag in self.kuma_tags:
                    print(f"{kuma_tag.name=} {tag=}")
                    if tag.name == kuma_tag.name or tag.uuid == kuma_tag.uuid:
                        add = False
                if add:
                    api.add_tag(
                        name=tag.name,
                        color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                    )
        except Exception as e:
            self.post_message(Errors(error=str(e)))

    def action_save_config(self) -> None:
        """Save the configuration to the JSON file."""
        data = {
            "url": self.url,
            "username": self.username,
            "password": self.password,
            "timeout": self.timeout,
            "layers": self.query_one("#layers_toggle").value,
            # "groups": self.query_one("#groups_toggle").value,
            "classes": self.query_one("#classes_toggle").value,
        }
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def action_quit(self) -> None:
        """Save the configuration to the JSON file when the app closes."""
        self.action_save_config()
        self.exit()


if __name__ == "__main__":
    app = UptimeKumaMVR()
    app.run()
