#!/usr/bin/env python3

# @raycast.schemaVersion 1
# @raycast.title Zip Selected in Finder
# @raycast.mode silent
# @raycast.packageName Utils
# @raycast.icon 🤐

import os
import subprocess
import zipfile
from datetime import datetime


def get_finder_selection():
    """Получает пути к выделенным файлам через AppleScript."""
    script = """
    tell application "Finder"
        set theSelection to selection as alias list
        set posixPaths to {}
        repeat with aFile in theSelection
            set end of posixPaths to POSIX path of aFile
        end repeat
        return posixPaths
    end tell
    """
    proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if proc.returncode != 0 or not proc.stdout.strip():
        return []
    # Пути разделяются запятыми в выводе AppleScript
    return [p.strip() for p in proc.stdout.split(", ") if p.strip()]


def main():
    selected_paths = get_finder_selection()

    if not selected_paths:
        print("Ничего не выделено в Finder")
        return

    # Определяем директорию (берем родительскую папку первого элемента)
    parent_dir = os.path.dirname(selected_paths[0])

    # Формируем имя архива (по дате или имени первого файла)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"archive_{timestamp}.zip"
    zip_path = os.path.join(parent_dir, zip_name)

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for path in selected_paths:
                if os.path.isfile(path):
                    zipf.write(path, os.path.basename(path))
                elif os.path.isdir(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            # Сохраняем структуру папок внутри архива
                            rel_path = os.path.relpath(
                                full_path, os.path.join(path, "..")
                            )
                            zipf.write(full_path, rel_path)

        print(f"Создан: {zip_name}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
