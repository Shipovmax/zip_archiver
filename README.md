# Zip Finder Selection

A macOS Python script that creates a timestamped ZIP archive from whatever is currently selected in Finder — works as a Raycast script command or standalone CLI tool.

---

## Features

- **Finder integration** — reads selection via AppleScript; no file picker, no drag-and-drop
- **Files and folders** — single files, multiple files, directories, or any mix
- **Recursive** — entire folder trees are preserved with relative paths inside the archive
- **Timestamped names** — `archive_20260424_143000.zip` saved next to the selected items; no overwrites
- **Special characters** — custom `|||` delimiter in AppleScript prevents comma-in-filename parsing errors
- **No dependencies** — stdlib only (`os`, `subprocess`, `zipfile`, `datetime`)

---

## Requirements

- macOS (AppleScript + Finder)
- Python 3.6+

---

## Usage

### Raycast (recommended)

1. Open Raycast → **Extensions** → **Script Commands**
2. Add `main.py` as a new Script Command
3. Select files or folders in Finder
4. Run **"Zip Selected in Finder"** from Raycast

### Terminal

```bash
# Select files in Finder first, then:
python3 main.py
```

---

## How It Works

```
Finder selection
      ↓ AppleScript (osascript)
  List of POSIX paths
      ↓
  zipfile.ZipFile (ZIP_DEFLATED)
      ↓
  archive_YYYYMMDD_HHMMSS.zip  →  same folder as selection
```

Files are archived by basename; directories are walked recursively with paths relative to their parent, so the folder name is preserved inside the archive.

---

## License

MIT

---

## Author

- GitHub: [Shipovmax](https://github.com/Shipovmax)
- Email: shipov.max@icloud.com
