# Build Your Own LOC Counter

This challenge is to build your own version of the tools `cloc`, `sloc`, and `scc`. These tools count lines of code and produce statistics on the number of lines in the source code: lines of actual code, comments, and empty lines.

Some also calculate the COCOMO 81 and COCOMO II estimates for the software being analyzed. If you’re not familiar with it, the COCOMO model was developed by Barry W. Boehm to estimate the effort, cost, and schedule for software projects. While not always practical for exact project planning, they’re an interesting way to get a feel for the size and scope of software.

Counting the lines of code in a software project sounds trivial and quite honestly seems like something you could do with a short bash command, i.e.:

```bash
find . -name '*.go' | xargs wc -l | sort -nr
```

However, if you want to do it accurately and fast, you start hitting some interesting computer science challenges.

---

## 📦 Project: `ccloc.py`

`ccloc.py` is a command-line tool written in Python that intelligently counts lines in source code files. It supports multiple programming languages and handles things like:

- Single-line and multi-line comments
- Code blocks inside Markdown files
- Multi-line strings in Python
- Hidden files/folders (with optional inclusion)
- File-wise and language-wise reports

---

## ✅ Features

- 🧠 **Language-aware parsing**
- 🧾 **Detailed stats per file (optional)**
- 📄 **Supports plaintext, markdown, and source code**
- 📂 **Recursive directory scanning**
- 🚫 **Ignores virtualenv and `.venv` by default**

---

## 📌 Supported Languages

| Language     | File Extension(s) |
|--------------|-------------------|
| Python       | `.py`             |
| Java         | `.java`           |
| C            | `.c`              |
| C++          | `.cpp`            |
| Go           | `.go`             |
| JavaScript   | `.js`             |
| Shell Script | `.sh`             |
| Markdown     | `.md`             |
| Plain Text   | `.txt`            |
| YAML         | `.yml`, `.yaml`   |

> You can easily extend support by modifying `LANGUAGE_CONFIGS` in the source code.

---

## 🚀 Usage

```bash
python ccloc.py [options] [path]
```

### Options:

- `-a`, `--all`  
  Include hidden files and directories (e.g. `.git`, `.venv`)

- `-d`, `--details`  
  Show detailed file-by-file statistics

- `path`  
  Path to the directory or file to analyze (defaults to current directory)

### Example:

```bash
python ccloc.py -d -a my_project/
```

This will scan `my_project/`, including hidden files, and show detailed output per file.

---

## 📊 Sample Output

```
-------------------------------------------------------------------------------------
File                                         Lines    Blanks   Comments       Code
-------------------------------------------------------------------------------------
main.py                                         100        20         30         50
src/utils.py                                     80        10         20         50
-------------------------------------------------------------------------------------
Language                              Files    Lines    Blanks   Comments       Code
-------------------------------------------------------------------------------------
Python                                   2       180        30         50        100
-------------------------------------------------------------------------------------
Total                                    2       180        30         50        100
-------------------------------------------------------------------------------------
```

---

## 🛠️ Installation

No special setup is needed. Just clone and run:

```bash
git clone https://github.com/mrsouravraj/CodingChallenges.git
cd CodingChallenges/CC-92-LOC_Counter
python ccloc.py
```

---

## 🔧 Extending Language Support

To add support for another language, update the `LANGUAGE_CONFIGS` dictionary in `ccloc.py` with appropriate values for:

- File extension
- Single-line comment prefix
- Multi-line comment delimiters
- String delimiters (if applicable)

Example for Rust:

```python
".rs": LanguageConfig(
    name="Rust",
    single_comment=["//"],
    multi_comment_start=["/*"],
    multi_comment_end=["*/"],
),
```

---