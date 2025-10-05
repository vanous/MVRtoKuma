class KumaFixture:
    def __init__(self, data=None):
        if data is None:
            return
        self.name = data.get("name", "")
        self.id = data.get("id", 0)
        self.description = data.get("description", "")
        self.tags = [tag.get("name") for tag in data.get("tags", [])]

    def __str__(self):
        return f"{self.name=} {self.id=} {self.description=} tags={','.join(self.tags)}"


class KumaTag:
    def __init__(self, data=None):
        if data is None:
            return
        self.id = data.get("id", 0)
        self.name = data.get("name", "")

    def __str__(self):
        return f"{self.name=} {self.id=}"
