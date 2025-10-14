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

### Testing git-bugs

- Issues are handled via https://github.com/git-bug/git-bug
- For pushing/pulling of bugs, either ssh based cloning must be used, or these [aliases](https://github.com/git-bug/git-bug/discussions/1332) can be used:

```
[alias]
	bugs = bug bug
	bug-users = bug user user
	open-bug = bug bug new
	push-bugs = "! fn(){ remote=origin; echo \"fetching bugs from '$remote' remote...\" >&2; git push  \"$remote\" --prune refs/bugs/* refs/identities/*; }; fn"
	pull-bugs = "! fn(){ remote=origin; echo \"fetching bugs from '$remote' remote...\" >&2; git fetch \"$remote\" \"refs/bugs/*:refs/bugs/*\" \"refs/identities/*:refs/identities/*\" && { [ ! -d .git/git-bug/cache/ ] || rm -r .git/git-bug/cache/; }; }; fn"
```
- I have no idea yet how to enable colaborators to pull/push bugs, probably by adding write access to the repo...?
- Try to use this and report any issues :)

### Upside

- GitHub independent, prevents noob questions and requests
- Local TUI and WEBUI

### Downside

- No notification about new issues/comments

## Run

```
uv run main.py
```

## Packaging

Initial pyinstaller setup

```
uv run pyinstaller --onefile --add-data "tui/*.css:tui" main.py
```
