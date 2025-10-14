<img  src="https://raw.githubusercontent.com/vanous/uptime-kuma-mvr/refs/heads/master/screenshot.png">

# UptimeKuma MVR

> [!Warning]
> Under Heavy Development 🚧

## Dev

```
uv run textual console
```

```
uv run textual run --dev main.py
```

## Bugs

- Issues are handled via https://github.com/git-bug/git-bug
- For pushing/pulling of bugs, ssh based cloning must be used
- I have no idea yet how to enable colaborators to pull/push bugs
- Try to use this and report any issues :)

## Run

```
uv run main.py
```

## Packaging

Initial pyinstaller setup

```
uv run pyinstaller --onefile --add-data "tui/*.css:tui" main.py
```
