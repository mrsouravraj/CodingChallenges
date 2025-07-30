import argparse

def count_words(content):
    words = content.split()
    return len(words)


def build_bloom_filter(file_path, fp_rate):
    pass


def main():
    parser = argparse.ArgumentParser(description="Spellchecker using Bloom filter.")
    parser.add_argument('-build', type=str, help='File containing words to add to the Bloom filter')

