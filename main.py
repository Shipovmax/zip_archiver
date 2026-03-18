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
from typing import List


def get_finder_selection() -> List[str]:
    """
    Retrieves the POSIX paths of the currently selected items in Finder
    using AppleScript.
    """
    # Use a specific delimiter to avoid issues with commas in file names
    delimiter = "|||"
    script = f"""
    tell application "Finder"
        set selectedItems to selection as alias list
        set posixPaths to {{}}
        repeat with aFile in selectedItems
            set end of posixPaths to POSIX path of aFile
        end repeat
        
        set oldDelimiters to AppleScript's text item delimiters
        set AppleScript's text item delimiters to "{delimiter}"
        set output to posixPaths as string
        set AppleScript's text item delimiters to oldDelimiters
        return output
    end tell
    """
    try:
        proc = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            check=True
        )
        output = proc.stdout.strip()
        if not output:
            return []
        return [p.strip() for p in output.split(delimiter) if p.strip()]
    except subprocess.CalledProcessError:
        return []


def create_archive(selected_paths: List[str]) -> None:
    """
    Creates a ZIP archive from the selected paths and saves it in the
    same directory.
    """
    if not selected_paths:
        print("No items selected in Finder.")
        return

    # Determine the directory (use the parent folder of the first item)
    # Filter out empty paths just in case
    selected_paths = [p for p in selected_paths if os.path.exists(p)]
    if not selected_paths:
        print("None of the selected paths exist.")
        return

    parent_dir = os.path.dirname(selected_paths[0])

    # Generate a unique archive name based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"archive_{timestamp}.zip"
    zip_path = os.path.join(parent_dir, zip_name)

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for item_path in selected_paths:
                if os.path.isfile(item_path):
                    # Write file, preserving its name
                    zipf.write(item_path, os.path.basename(item_path))
                elif os.path.isdir(item_path):
                    # Write directory and its contents recursively
                    for root, _, files in os.walk(item_path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            # Maintain the relative structure inside the archive
                            # We use the parent of item_path to include the folder itself
                            rel_path = os.path.relpath(
                                full_path, os.path.dirname(item_path)
                            )
                            zipf.write(full_path, rel_path)

        print(f"Archive created: {zip_name}")
    except Exception as error:
        print(f"Error creating archive: {error}")


def main():
    """Main execution point for the Raycast script."""
    selected_paths = get_finder_selection()
    create_archive(selected_paths)


if __name__ == "__main__":
    main()
