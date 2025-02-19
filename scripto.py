import os
import sys
import fnmatch
import mimetypes
import urllib.parse
import webbrowser

# Directories to always ignore
DEFAULT_IGNORED_DIRS = {"node_modules", "target", ".mvn", "dist", "build", "venv", ".git", "__pycache__"}

def load_gitignore(folder_path):
    """Reads .gitignore and returns a set of patterns to ignore."""
    gitignore_file = os.path.join(folder_path, '.gitignore')
    ignore_patterns = set()

    if os.path.exists(gitignore_file):
        with open(gitignore_file, 'r', encoding='utf-8') as gitignore:
            for line in gitignore:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore comments and empty lines
                    ignore_patterns.add(line)
    
    return ignore_patterns

def is_ignored(file_path, ignore_patterns, root_folder):
    """Checks if a file or folder matches any ignore pattern."""
    rel_path = os.path.relpath(file_path, root_folder)  # Get relative path for matching

    # Check against predefined ignored directories
    for ignored_dir in DEFAULT_IGNORED_DIRS:
        if ignored_dir in rel_path.split(os.sep):  # Ensures we skip entire directories
            return True

    # Check against .gitignore patterns
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(rel_path, pattern) or rel_path.startswith(pattern):
            return True

    return False

def is_binary_file(file_path):
    """Uses mimetypes and a binary read check to determine if a file is binary."""
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type and not mime_type.startswith("text"):  # If mimetype is non-text, skip
        return True
    
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:  # Null bytes typically indicate a binary file
                return True
    except Exception:
        return True  # Assume binary if an error occurs

    return False

def extract_text_from_folder(folder_path, recursive=True):
    """
    Extracts text from all non-ignored files in a folder (and optionally its subfolders)
    and combines it into a single output file.

    Args:
        folder_path (str): The path to the folder containing the files.
        recursive (bool): Whether to scan subdirectories recursively.
    """
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_directory, 'combined_text.txt')

    ignore_patterns = load_gitignore(folder_path)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(folder_path):
            # Apply .gitignore filtering and always-ignore directories
            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), ignore_patterns, folder_path)]

            for filename in files:
                file_path = os.path.join(root, filename)

                # Ignore files listed in .gitignore and package/dependency files
                if is_ignored(file_path, ignore_patterns, folder_path):
                    continue
                
                # Skip binary files (e.g., .jar, .class, .png, .ico, .pdf)
                if is_binary_file(file_path):
                    print(f"Skipping binary file: {file_path}")
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(f"--- Start of file: {file_path} ---\n")
                        outfile.write(infile.read())
                        outfile.write(f"\n--- End of file: {file_path} ---\n\n")
                except UnicodeDecodeError:
                    print(f"Skipping file {file_path} due to encoding issues.")

            if not recursive:
                break  # Stop after processing the top-level directory

    return output_file

def print_directory_tree(path, indent=''):
    """Prints the directory tree starting from the given path."""
    try:
        items = sorted([item for item in os.listdir(path) if item not in DEFAULT_IGNORED_DIRS])
    except OSError as e:
        print(f"{indent}[Error accessing: {e}]")
        return

    for index, item in enumerate(items):
        full_path = os.path.join(path, item)
        is_last = index == len(items) - 1
        connector = '└── ' if is_last else '├── '
        
        print(f"{indent}{connector}{item}")

        if os.path.isdir(full_path):
            new_indent = indent + ('    ' if is_last else '│   ')
            print_directory_tree(full_path, new_indent)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py <folder_path> [--recursive] [--tree]")
        sys.exit(1)

    folder_path = sys.argv[1]
    recursive = "--recursive" in sys.argv
    show_tree = "--tree" in sys.argv

    if show_tree:
        print(f"📁 Directory tree for: {folder_path}\n")
        print_directory_tree(folder_path)
        sys.exit(0)

    output_file = extract_text_from_folder(folder_path, recursive)

    # Correct Windows file path format
    output_file_url = f"file:///{output_file.replace(os.sep, '/')}"
    
    # Print a clickable PowerShell command
    print(f"\n✅ Text extraction complete! Open file:")
    print(f"📂 Click here: \033[4;34m{output_file_url}\033[0m\n")
    print(f"📌 Or run this command in PowerShell to open the file:\n   start {output_file}\n")

    # Automatically open the file in the default text editor (Windows only)
    if sys.platform == "win32":
        os.startfile(output_file)
