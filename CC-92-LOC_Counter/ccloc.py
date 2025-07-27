import os
import argparse
from collections import defaultdict


class LanguageConfig:
    def __init__(
        self,
        name,
        single_comment=None,
        multi_comment_start=None,
        multi_comment_end=None,
        multi_string_delims=None,
        is_plain_text=False,
        is_markdown=False,
    ):
        self.name = name
        self.single_comment = single_comment or []
        self.multi_comment_start = multi_comment_start or []
        self.multi_comment_end = multi_comment_end or []
        self.multi_string_delims = multi_string_delims or []
        self.is_plain_text = is_plain_text
        self.is_markdown = is_markdown


IGNORE_DIRS = {"venv", ".venv"}


class GenericCodeAnalyzer:
    # Define language configs; add new languages here as needed
    LANGUAGE_CONFIGS = {
        ".py": LanguageConfig(
            name="Python",
            single_comment=["#"],
            multi_string_delims=['"""', "'''"],
        ),
        ".java": LanguageConfig(
            name="Java",
            single_comment=["//"],
            multi_comment_start=["/*"],
            multi_comment_end=["*/"],
        ),
        ".c": LanguageConfig(
            name="C",
            single_comment=["//"],
            multi_comment_start=["/*"],
            multi_comment_end=["*/"],
        ),
        ".cpp": LanguageConfig(
            name="C++",
            single_comment=["//"],
            multi_comment_start=["/*"],
            multi_comment_end=["*/"],
        ),
        ".go": LanguageConfig(
            name="Go",
            single_comment=["//"],
            multi_comment_start=["/*"],
            multi_comment_end=["*/"],
        ),
        ".js": LanguageConfig(
            name="JavaScript",
            single_comment=["//"],
            multi_comment_start=["/*"],
            multi_comment_end=["*/"],
        ),
        ".sh": LanguageConfig(
            name="Shell Script",
            single_comment=["#"],
        ),
        ".md": LanguageConfig(
            name="Markdown",
            is_markdown=True,
        ),
        ".txt": LanguageConfig(
            name="Plain Text",
            is_plain_text=True,
        ),
        ".yaml": LanguageConfig(
            name="YAML",
            single_comment=["#"],
        ),
        ".yml": LanguageConfig(
            name="YAML",
            single_comment=["#"],
        ),
        # Add more languages here
    }

    def __init__(self, path, include_hidden=False, allowed_extensions=None):
        self.path = path
        self.include_hidden = include_hidden
        # Default allowed extensions = keys from language configs
        if allowed_extensions is None:
            self.allowed_extensions = set(self.LANGUAGE_CONFIGS.keys())
        else:
            self.allowed_extensions = {
                ext if ext.startswith(".") else f".{ext}"
                for ext in map(str.lower, allowed_extensions)
            }

        self.results = []
        self.results_total = defaultdict(lambda: defaultdict(int))

        # Totals across all languages
        self._total_files = 0
        self._total_lines = 0
        self._total_blank = 0
        self._total_comments = 0
        self._total_code = 0

    def is_hidden(self, path):
        """Check if any part of the path is hidden (starts with a dot)."""
        return any(part.startswith(".") for part in path.split(os.sep))

    def detect_language(self, filename):
        """Return LanguageConfig for the file extension or None if unknown."""
        _, ext = os.path.splitext(filename)
        return self.LANGUAGE_CONFIGS.get(ext.lower())

    def analyze_file(self, filepath, lang_config):
        if lang_config is None:
            return self._analyze_plain_text(filepath)
        if lang_config.is_markdown:
            return self._analyze_markdown(filepath)
        if lang_config.is_plain_text:
            return self._analyze_plain_text(filepath)
        return self._analyze_code_file(filepath, lang_config)

    def _analyze_plain_text(self, filepath):
        total = blank = non_blank = 0
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    total += 1
                    if line.strip():
                        non_blank += 1
                    else:
                        blank += 1
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")
        return total, blank, 0, non_blank

    def _analyze_markdown(self, filepath):
        total = blank = comments = code = 0
        in_code_block = False
        fence = None

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    total += 1
                    stripped = line.rstrip("\n")

                    if stripped.startswith(("```", "~~~")):
                        fence_mark = stripped[:3]
                        if not in_code_block:
                            in_code_block = True
                            fence = fence_mark
                        elif fence == fence_mark:
                            in_code_block = False
                            fence = None
                        blank += 1  # Fence lines count as blank/comment
                        continue

                    if not stripped.strip():
                        blank += 1
                    elif in_code_block:
                        code += 1
                    else:
                        comments += 1
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")

        return total, blank, comments, code

    def _analyze_code_file(self, filepath, lang_config):
        total = blank = comments = code = 0
        in_multi_comment = False
        in_multi_string = False
        current_string_delim = None

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    total += 1
                    stripped = line.strip()

                    if not stripped:
                        blank += 1
                        continue

                    # Multi-line string delimiters (Python style)
                    if lang_config.multi_string_delims:
                        if in_multi_string:
                            comments += 1
                            if stripped.endswith(current_string_delim):
                                in_multi_string = False
                                current_string_delim = None
                            continue
                        for delim in lang_config.multi_string_delims:
                            if stripped.startswith(delim):
                                in_multi_string = True
                                current_string_delim = delim
                                comments += 1
                                break
                        if in_multi_string:
                            continue

                    # Multi-line comments (C-style)
                    if (
                        lang_config.multi_comment_start
                        and lang_config.multi_comment_end
                    ):
                        if in_multi_comment:
                            comments += 1
                            if any(
                                end in stripped for end in lang_config.multi_comment_end
                            ):
                                in_multi_comment = False
                            continue
                        if any(
                            start in stripped
                            for start in lang_config.multi_comment_start
                        ):
                            comments += 1
                            if not any(
                                end in stripped for end in lang_config.multi_comment_end
                            ):
                                in_multi_comment = True
                            continue

                    # Single line comments
                    if any(
                        stripped.startswith(sc) for sc in lang_config.single_comment
                    ):
                        comments += 1
                        continue

                    # Otherwise code
                    code += 1

        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")

        return total, blank, comments, code

    def _analyze_and_store(self, filepath, base_path=None):
        if not self.include_hidden and self.is_hidden(filepath):
            return
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in self.allowed_extensions:
            return
        lang_config = self.detect_language(filepath)
        if lang_config is None:
            return

        total, blank, comments, code = self.analyze_file(filepath, lang_config)
        rel_path = (
            os.path.relpath(filepath, base_path)
            if base_path
            else os.path.basename(filepath)
        )

        stats = self.results_total[lang_config.name]
        stats["files"] += 1
        stats["total"] += total
        stats["blank"] += blank
        stats["comments"] += comments
        stats["code"] += code

        self._total_files += 1
        self._total_lines += total
        self._total_blank += blank
        self._total_comments += comments
        self._total_code += code

        self.results.append((rel_path, total, blank, comments, code))

    def scan(self):
        if os.path.isfile(self.path):
            self._analyze_and_store(self.path)
        else:
            for root, dirs, files in os.walk(self.path):
                dirs[:] = [d for d in dirs if d.lower() not in IGNORE_DIRS]
                for file in files:
                    full_path = os.path.join(root, file)
                    self._analyze_and_store(full_path, base_path=self.path)

    def print_report(self, detailed=False):
        if detailed:
            print("─" * 85)
            print(
                f"{'File':<45} {'Lines':>8} {'Blanks':>9} {'Comments':>10} {'Code':>10}"
            )
            print("─" * 85)
            for file, total, blank, comments, code in self.results:
                print(f"{file:<45} {total:>8} {blank:>9} {comments:>10} {code:>10}")

        print("─" * 85)
        print(
            f"{'Language':<35} {'Files':>8} {'Lines':>8} {'Blanks':>9} {'Comments':>10} {'Code':>10}"
        )
        print("─" * 85)
        for language, stats in self.results_total.items():
            print(
                f"{language:<35} "
                f"{stats['files']:>8} "
                f"{stats['total']:>8} "
                f"{stats['blank']:>9} "
                f"{stats['comments']:>10} "
                f"{stats['code']:>10}"
            )
        print("─" * 85)
        print(
            f"{'Total':<35} "
            f"{self._total_files:>8} "
            f"{self._total_lines:>8} "
            f"{self._total_blank:>9} "
            f"{self._total_comments:>10} "
            f"{self._total_code:>10}"
        )
        print("─" * 85)


def main():
    parser = argparse.ArgumentParser(
        description="Count lines in files with language-aware parsing, including Markdown and plain text."
    )
    parser.add_argument(
        "path", nargs="?", default=os.getcwd(), help="Directory to scan"
    )
    parser.add_argument(
        "-a", "--all", action="store_true", help="Include hidden files/folders"
    )
    parser.add_argument(
        "-d",
        "--details",
        action="store_true",
        help="Include file-wise details (default: False)",
    )
    args = parser.parse_args()

    analyzer = GenericCodeAnalyzer(args.path, include_hidden=args.all)
    analyzer.scan()
    analyzer.print_report(args.details)


if __name__ == "__main__":
    main()
