# ![SLC](/images/icon.png) Simple Log Cleaner
The utility for filtering log files based on specified strings.

## Features
- Filtering of `.log` and `.txt` files.
- Support for multiple parameters (each on a new line).
- Filtering logic: a line must contain all specified parameters.
- View results in the interface.
- Copy results to the clipboard.
- Save results to a file.
- Built-in example.
- Dark / light theme.
- Keyboard shortcuts:
  - `Ctrl+C` - copy.
  - `Ctrl+V` - paste.
  - `Ctrl+X` - cut.
  - `Ctrl+A` - select all.

## Gallery
<img title="Light theme" src="/images/overview/light_theme.png" width="300"> <img title="Dark theme" src="/images/overview/dark_theme.png" width="300"> <img title="One-line query" src="/images/overview/one-line_query.png" width="300"> <img title="Multi-line query" src="/images/overview/multi-line_query.png" width="300"> <img title="Context menu (input field)" src="/images/overview/context_menu_(input_field).png" width="300"> <img title="Context menu (output field)" src="/images/overview/context_menu_(output_field).png" width="300">

## How to use
1. Run `main.py` or the corresponding `.exe` file.
2. Click `Select .log File` and select a file.
3. Enter the filter parameters (one per line).
4. Click `Filter Log`.

The result will appear in the output field.

## Example parameters (Minecraft)
```
[Server thread/INFO]
[Not Secure]
<Steve>
joined the game
```
## Installation
**Requirements:**
- Python 3.x

**Dependencies:**
```
pip install -U pyperclip
```
or use
```
pip install -r requirements.txt
```
in project folder

> [!NOTE]
> - The file is read in UTF-8 (errors are ignored).
> - Empty parameters are ignored.
> - If no file is selected, filtering will not be performed.

## Roadmap
- [x] GUI.
- [x] Uploading `.log` / `.txt` files.
- [x] Filtering by multiple criteria (`AND` logic).
- [x] Displaying the result.
- [x] Copy to clipboard.
- [x] Save to file.
- [x] Dark / light theme.
- [x] Context menu + hotkeys.
- [x] Example (`example.log` + random parameters from the list).
- [ ] Add new filtering options:
  - [ ] "Any match" mode (using `any` instead of `all`).
  - [ ] Support for conditional logic (`OR`, `AND`, `CUSTOM`, etc.).
  - [ ] Case-sensitive (toggle).
- [ ] Progress bar.
- [ ] Highlighting matches in the results.
- [ ] Real-time coincidence counter (no pop-ups).
- [ ] Drag & Drop a file.
- [ ] Streaming processing of large files (>100 MB).
- [ ] Removing duplicates (toggle).
- [ ] Line limit (toggle).
- [ ] Console mode.
- [ ] Modularization:
  - [ ] Plugin-based filter system.
  - [ ] Configuration (`.json` / `.yaml`).
- [ ] Logging system.
- [ ] Filters via the UI (checkboxes, fields).
- [ ] Search within the result.
- [ ] Presetting:
  - [ ] Saving filter sets (presets).
  - [ ] Quick preset switching.
  - [ ] Custom themes.
  - [ ] Presets for:
    - [ ] Minecraft.
    - [ ] Server logs.
    - [ ] System logs.
- [ ] Field separation (timestamp, level, message).

## License
This project is licensed under the [Attribution-NonCommercial-NoDerivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.ru) license. See the [LICENSE](https://github.com/Cicada535/simple-log-cleaner/blob/master/LICENSE) file for details.
