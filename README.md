# ContextWeaver

**ContextWeaver** is a CLI that scans a local repository and produces a single, well-structured text snapshot that’s easy for LLMs to understand.

It includes:
- Git info 
- Project structure tree
- File contents 
- Summary stats (files, lines), optional token estimate

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
##License
This project is licensed under the MIT License.
