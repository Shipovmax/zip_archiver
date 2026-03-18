# Zip Finder Selection

A simple and efficient Python script designed to create a ZIP archive from the currently selected files or folders in the macOS Finder. This script is optimized for use as a Raycast script but can also be run independently.

## Features

- **Finder Integration:** Uses AppleScript to dynamically fetch current selections from the macOS Finder.
- **Robustness:** Handles files and directories with complex characters (including spaces and commas) by using a custom delimiter for AppleScript output parsing.
- **Recursive Zipping:** Automatically includes all subdirectories and files within selected folders while maintaining the relative directory structure.
- **Timestamped Archives:** Creates unique ZIP file names (e.g., `archive_20260318_143000.zip`) to prevent overwriting existing files.
- **English Localization:** Fully localized comments, documentation, and user output for international usability.

## Prerequisites

- **macOS:** Requires macOS to interact with Finder via AppleScript.
- **Python 3.6+:** The script uses standard libraries (`os`, `subprocess`, `zipfile`, `datetime`).

## Usage

### As a Raycast Script
1.  Open Raycast and navigate to **Extensions**.
2.  Add a new **Script Command**.
3.  Point it to `main.py` or the directory containing the script.
4.  Run "Zip Selected in Finder" from the Raycast command window.

### Manually
You can run the script from the terminal:
```bash
python3 main.py
```
*Note: Make sure you have something selected in Finder before running.*

## Code Structure

- `main.py`: The main entry point containing the logic for:
  - Fetching selection paths via `osascript`.
  - Creating and compressing the ZIP archive using `zipfile`.
  - Handling errors and providing feedback to the user.

## Technical Details

- **AppleScript Delimiters:** Used `AppleScript's text item delimiters` to ensure that paths are parsed correctly even if they contain special characters.
- **PEP 8 Compliance:** The code follows Python's standard style guide for readability and maintainability.
- **Type Hinting:** Includes type annotations for better IDE support and code clarity.

## License

MIT
