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
    - it seems https workflow is also supported, but it is better to create some aliases: https://github.com/git-bug/git-bug/discussions/1332
        - i have tested the aliases and pull does not really work for me
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
