# Build Your Own wc Tool

This challenge is to build your own version of the Unix command line tool wc!

The Unix command line tools are a great metaphor for good software engineering and they follow the Unix Philosophies of:

1. Writing simple parts connected by clean interfaces - each tool does just one thing and provides a simple CLI that handles text input from either files or file streams.
2. Design programs to be connected to other programs - each tool can be easily connected to other tools to create incredibly powerful compositions.

# 🧮 ccwc — Custom `wc` Tool in Python

A Python-based reimplementation of the Unix `wc` (word count) command. This tool displays the number of **lines**, **words**, **characters**, and **bytes** in a file — just like the original `wc`.

---

## 🚀 Features

- Supports counting:
  - Lines (`-l`)
  - Words (`-w`)
  - Characters (`-m`)
  - Bytes (`-c`)
- Defaults to showing all counts if no flags are passed
- Accepts a filename as input
- Simple and easy to extend

---

## 🛠 Usage

```bash
python ccwc.py [options] filename
