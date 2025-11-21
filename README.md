# ContextWeaver

**ContextWeaver** is a command-line tool designed to help developers package and share their codebase with Large Language Models (LLMs) like ChatGPT.
When you want to ask an AI tool about your code, it’s often hard to know what and how much to copy. ContextWeaver automates this process by scanning your files, filtering relevant content, and combining everything into a single, ready-to-share document.

ContextWeaver solves this by:
- Scanning your repository or selected files
- Collecting metadata and structure automatically
- Embedding file contents into a single, organized text document
- Supporting filtering (--include, --exclude), size limits, and token counts so you can fine-tune what gets included.
  
The result is a ready-to-share snapshot of your repo that you can paste into an LLM for debugging, documentation, or collaboration.

---

## Installation

```bash
git clone https://github.com/kkrishnan10/ContextWeaver
cd ContextWeaver
# virtual env
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

Install from PyPI
pip install contextweaver

Install from TestPyPI
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple contextweaver

```

## Usage

```bash
# Analyze current directory
python src/main.py .

# Analyze a specific directory
python src/main.py ./src

# Analyze specific files
python src/main.py src/main.py README.md

# Save output to a file
python src/main.py . -o snapshot.txt

# Estimate token count (~chars/4) printed to stderr
python src/main.py . --tokens

# Only include certain file patterns (comma-separated)
python src/main.py . --include "*.py,*.md"

# Generate a snapshot of your codebase
python3 src/main.py . -V -l --tokens --include=*.py,*.md -o snapshot.txt

# Command Line Usage (After Installing via pip)
Once installed, run:
contextweaver --help

# Generate a snapshot of the current folder
contextweaver . -o snapshot.txt

# Analyze a specific folder
contextweaver ./src -o src_snapshot.txt

```
## Features

### Verbose Mode

```bash
# Show progress messages to stderr while scanning
python src/main.py . --verbose
# or shorter
python src/main.py . -V
```
### Line Numbers

```bash
# Prefix each line of file content with its 1-based line number
python src/main.py . --line-numbers
# or shorter
python src/main.py . -l
```
### Combined Usage

```bash
# Enable both verbose logging and line numbers
python src/main.py . -V -l
```
---
## What's New in Refactored 0.1

In this refactored version, the codebase has been redesigned for **maintainability**, **readability**, and **extensibility**.  
The main improvements include:

- **Separated CLI logic** into `src/cli.py`  
- **Introduced modular file scanning and filtering** (`scanner.py`, `filters.py`)  
- **Added utility helpers** for clean I/O and formatting (`utils.py`, `formatter.py`)  
- **Improved variable naming** and reduced duplication  
- **Enhanced argument parsing** for better usability  

These changes make ContextWeaver easier to maintain and prepare it for future enhancements such as automated testing and configuration file support.

---

---

## Troubleshooting

```md

### ERROR: Requires-Python >=3.10
Your Python version is too old. Use Python 3.10+ or create a new venv with it.

### contextweaver: command not found
Your virtual environment is not active or pip install didn't update your PATH.

### LibreSSL warning on macOS
Safe to ignore — does not affect installation or usage.

```
## License
This project is licensed under the MIT License.
