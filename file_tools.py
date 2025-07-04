import os


FILE_TOOLS = {
    "create_file": {
        "name": "create_file",
        "description": "Create a new file at the specified path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The path where the file should be created."}
            },
            "required": ["path"]
        }
    },
    "create_directory": {
        "name": "create_directory",
        "description": "Create a new directory at the specified path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The path where the directory should be created."}
            },
            "required": ["path"]
        }
    },
    "delete_file": {
        "name": "delete_file",
        "description": "Delete a file at the specified path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The path of the file to delete."}
            },
            "required": ["path"]
        }
    },
    "does_file_exist": {
        "name": "does_file_exist",
        "description": "Check if a file exists at the specified path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The path of the file to check."}
            },
            "required": ["path"]
        }
    },
    "get_directory_tree": {
        "name": "get_directory_tree",
        "description": "Return the tree structure of a directory, including hidden files.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The directory path to get the tree structure for."},
                "prefix": {"type": "string", "description": "Prefix for formatting the tree structure.", "default": ""}
            },
            "required": ["path"]
        }
    },
    "read_file": {
        "name": "read_file",
        "description": "Read the content of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The path of the file to read."}
            },
            "required": ["path"]
        }
    },
    "write_file": {
        "name": "write_file",
        "description": "Write content to a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The path of the file to write to."},
                "content": {"type": "string", "description": "The content to write to the file."}
            },
            "required": ["path", "content"]
        }
    },
    "append_to_file": {
        "name": "append_to_file",
        "description": "Append content to a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The path of the file to append to."},
                "content": {"type": "string", "description": "The content to append to the file."}
            },
            "required": ["path", "content"]
        }
    },
    "copy_file": {
        "name": "copy_file",
        "description": "Copy a file from source to destination.",
        "parameters": {
            "type": "object",
            "properties": {
                "src": {"type": "string", "description": "The source file path."},
                "dst": {"type": "string", "description": "The destination file path."}
            },
            "required": ["src", "dst"]
        }
    },
    "move_file": {
        "name": "move_file",
        "description": "Move a file from source to destination.",
        "parameters": {
            "type": "object",
            "properties": {
                "src": {"type": "string", "description": "The source file path."},
                "dst": {"type": "string", "description": "The destination file path."}
            },
            "required": ["src", "dst"]
        }
    }
}


def create_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print(f"File created at {path}")

def create_directory(path):
    """Create a directory if it does not already exist.

    Args:
        path (str): The directory path to create.

    Raises:
        OSError: If the directory cannot be created.
    """
    os.makedirs(path, exist_ok=True)
    print(f"Directory created at {path}")

def delete_file(path):
    """Delete a file at the specified path.

    Args:
        path (str): The file path to delete.

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be deleted.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at {path} does not exist.")

    os.remove(path)
    print(f"File deleted at {path}")

def does_file_exist(path):
    """Check if a file exists at the specified path.

    Args:
        path (str): The file path to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(path)

def get_directory_tree(path, prefix=''):
    """Return the tree structure of a directory, including hidden files."""
    tree_str = ''
    entries = sorted(os.listdir(path))
    entries_count = len(entries)
    for idx, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        connector = '└── ' if idx == entries_count - 1 else '├── '
        tree_str += f"{prefix}{connector}{entry}\n"
        if os.path.isdir(full_path):
            extension = '    ' if idx == entries_count - 1 else '│   '
            tree_str += get_directory_tree(full_path, prefix + extension)
    return tree_str

def read_file(path):
    """Read the content of a file.

    Args:
        path (str): The file path to read.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at {path} does not exist.")

    with open(path, 'r') as f:
        content = f.read()

    return content

def write_file(path, content):
    """Write content to a file.

    Args:
        path (str): The file path to write to.
        content (str): The content to write to the file.

    Raises:
        OSError: If the file cannot be written.
    """
    with open(path, 'w') as f:
        f.write(content)
    print(f"Content written to {path}")


def append_to_file(path, content):
    """Append content to a file.

    Args:
        path (str): The file path to append to.
        content (str): The content to append to the file.

    Raises:
        OSError: If the file cannot be appended.
    """
    with open(path, 'a') as f:
        f.write(content)
    print(f"Content appended to {path}")

def copy_file(src, dst):
    """Copy a file from source to destination.

    Args:
        src (str): The source file path.
        dst (str): The destination file path.

    Raises:
        FileNotFoundError: If the source file does not exist.
        OSError: If the file cannot be copied.
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"The source file at {src} does not exist.")

    with open(src, 'rb') as f_src:
        content = f_src.read()

    with open(dst, 'wb') as f_dst:
        f_dst.write(content)

    print(f"File copied from {src} to {dst}")

def move_file(src, dst):
    """Move a file from source to destination.

    Args:
        src (str): The source file path.
        dst (str): The destination file path.

    Raises:
        FileNotFoundError: If the source file does not exist.
        OSError: If the file cannot be moved.
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"The source file at {src} does not exist.")

    os.rename(src, dst)
    print(f"File moved from {src} to {dst}")
