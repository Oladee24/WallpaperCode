

# Live Desktop WallpaperCode

A small Python script that builds a custom desktop wallpaper showing my GitHub activity, a to-do list, and a calendar, then sets it as the Windows wallpaper automatically.

## What it shows

- **GitHub card:** public repos, followers, following, and stars earned
- **To-do list:** read from a plain `todo.txt` file (italic green, with ticked and unticked items)
- **Calendar:** the current month with today highlighted in sage
- **Contribution heatmap:** the last year of GitHub activity

## Requirements

- Windows 10 or 11
- Python 3.9+
- Libraries: `pillow` and `requests`

```
pip install pillow requests
```

## Setup

1. Put `wallpaper.py` and `todo.txt` in the same folder.
2. In `wallpaper.py`, set your GitHub username:
   ```python
   USER = "your-username"
   ```
3. Run it:
   ```
   python wallpaper.py
   ```

The wallpaper changes straight away, and a copy is saved as `wallpaper.png` in the same folder.

## Editing the to-do list

Add one task per line in `todo.txt`. Start a line with `x ` to mark it done:

```
Finish k8s ConfigMap project
x Update LinkedIn post
Apply to 3 cloud engineer roles
```

Only the first 8 lines are shown.

## Auto-update (Windows Task Scheduler)

1. Run `where pythonw` in a terminal and copy the path.
2. Open Task Scheduler, choose **Create Basic Task**, and name it "Wallpaper".
3. Action: **Start a program**
   - Program: the `pythonw.exe` path
   - Arguments: full path to `wallpaper.py`
   - Start in: the project folder
4. In the task's **Triggers**, tick **Repeat task every 30 minutes**, **Indefinitely**.
5. Leave it on **Run only when user is logged on**.

## Customising

| What | Where |
|------|-------|
| Colours | `TEXT`, `MUTED`, `ACCENT`, `TODO_GREEN` at the top of the script |
| Fonts | the `font()` function (uses Segoe UI, falls back to Arial) |
| Screen size | `W, H` (default 1920×1080) |
| Card positions | the `card((x1, y1, x2, y2))` calls |

Cards are placed to stay clear of desktop icons on the left and the taskbar at the bottom.


## Notes

- The contribution heatmap comes from a free third-party service (`github-contributions-api.jogruber.de`) because GitHub's official API needs a login token for that data. It only reads public activity.
- Windows only, because it uses the Windows API to set the wallpaper.

## Contributions for later

- Make it interactive (clickable to-do list, hover details on the heatmap) by rebuilding it as an HTML page in [Lively Wallpaper](https://github.com/rocksdanister/lively)
- Show a daily quote or weather
- Pull tasks from Notion or a calendar instead of a text file
