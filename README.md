# ContextWeaver

**ContextWeaver** is a command-line tool designed to help developers package and share their codebase with Large Language Models (LLMs) like ChatGPT.
When you want to ask an AI tool about your code, it’s often hard to know what and how much to copy. 

ContextWeaver solves this by:
- Scanning your repository or selected files
- Collecting metadata and structure automatically
- Embedding file contents into a single, organized text document
- Supporting filtering options like file patterns and recent changes
- Providing size limits and token counts so you can fine-tune what gets included
  
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

# Only include files modified in the last 7 days
python src/main.py . --recent

# Short form of recent flag
python src/main.py . -r

# Combine recent filter with output file
python src/main.py . --recent -o recent-changes.txt
```

## Features

### Recent Changes Filter
The `--recent` (or `-r`) flag filters the output to only include files that have been modified within the last 7 days. This is particularly useful when:
- Working with large codebases and wanting to focus on active development areas
- Sharing recent changes with team members or AI assistants
- Debugging issues related to recent modifications

When using the recent filter, ContextWeaver will:
- Show modification timestamps for each file (e.g., "Modified: 2 hours ago")
- Display the total number of recent files found
- Add a note in the summary indicating recent filtering is active

## License
This project is licensed under the MIT License.
