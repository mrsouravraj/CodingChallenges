import argparse

def count_content(content, count_lines, count_words, count_chars, count_bytes):
    lines = content.splitlines()
    words = content.split()
    char_count = len(content)
    byte_count = len(content.encode('utf-8'))

    results = []
    if count_lines:
        results.append(str(len(lines)))
    if count_words:
        results.append(str(len(words)))
    if count_chars:
        results.append(str(char_count))
    if count_bytes:
        results.append(str(byte_count))

    return results

def main():
    parser = argparse.ArgumentParser(description="Custom wc tool (ccwc.py)")
    parser.add_argument("file", nargs="?", type=argparse.FileType('r'), default="-", help="Input file (or STDIN)")
    parser.add_argument("-l", action="store_true", help="Print line count")
    parser.add_argument("-w", action="store_true", help="Print word count")
    parser.add_argument("-m", action="store_true", help="Print character count")
    parser.add_argument("-c", action="store_true", help="Print byte count")

    args = parser.parse_args()

    content = args.file.read()

    # If no flag is provided, print all
    if not (args.l or args.w or args.m or args.c):
        args.l = args.w = args.m = True

    result = count_content(content, args.l, args.w, args.m, args.c)
    print(" ".join(result), end="")

    if args.file.name != "<stdin>":
        print(" " + args.file.name)
    else:
        print()

if __name__ == "__main__":
    main()
