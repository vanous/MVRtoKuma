from textual.message import Message


class MvrParsed(Message):
    """Message sent when monitors are fetched from the API."""

    def __init__(self, fixtures: list | None = None, tags: list | None = None) -> None:
        self.fixtures = fixtures
        self.tags = tags
        super().__init__()


class Errors(Message):
    """Message sent when monitors are fetched from the API."""

    def __init__(self, error: str | None = None) -> None:
        self.error = error
        super().__init__()


class DevicesDiscovered(Message):
    """Message sent when monitors are fetched from the API."""

    def __init__(self, devices: list | None = None) -> None:
        self.devices = devices
        super().__init__()
