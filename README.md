# Pierex

Pierex is a lightweight file watcher for Python development. It monitors files and directories for changes and automatically restarts the given Python script when modifications occur. This helps streamline the development process by reducing manual restarts.

## Features
- Watches for file changes in the specified directories
- Automatically restarts the Python script when a change is detected
- Improves development workflow by reducing manual intervention

## Installation
```sh
pip install pierex
```

## Usage
```sh
pierex your_script.py
```

### Optional Flags
- `-d`, `--dir <path>`: Specify the directory to watch (default: current directory)
- `-e`, `--ext <ext1,ext2>`: Watch specific file extensions (default: `.py`)

Example:
```sh
pierex -d src -e py,toml my_script.py
```

## Requirements
- Python 3.6+

## How It Works
1. Pierex monitors the specified directory for changes in relevant files.
2. When a change is detected, it stops the running Python script.
3. It restarts the script automatically to reflect the changes.

## Contributing
Pull requests and feature suggestions are welcome! Feel free to open an issue if you find a bug or have an idea to improve Pierex.

## License
MIT License

