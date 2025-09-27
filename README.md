# ContextWeaver

**ContextWeaver** is a command-line tool designed to help developers package and share their codebase with Large Language Models (LLMs) like ChatGPT.
When you want to ask an AI tool about your code, it’s often hard to know what and how much to copy. 

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

## License
This project is licensed under the MIT License.
