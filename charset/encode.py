import argparse

def check_encoding(entries, encodings, filter_language=None):
    for encoding in encodings:
        total_bytes = 0
        good_count = 0
        bad_count = 0

        for language, word in entries:
            if filter_language and language.lower() != filter_language.lower():
                continue

            try:
                encoded = word.encode(encoding)
                byte_count = len(encoded)
                hex_bytes = " ".join(f"{b:02X}" for b in encoded)
                print(f"In {encoding} {language} {word} is good:  {hex_bytes} ({byte_count} bytes)")
                total_bytes += byte_count
                good_count += 1
            except UnicodeEncodeError:
                print(f"In {encoding} {language} {word} is bad")
                bad_count += 1

        if not filter_language:
            print(f"\n--- Summary for {encoding} ---")
            print(f"Good dogs: {good_count} (total {total_bytes} bytes)")
            print(f"Bad dogs: {bad_count}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check encoding compatibility of dog words.")
    parser.add_argument("filename", help="CSV file (language,word)")
    parser.add_argument("encodings", nargs="+", help="One or more encodings to test")
    parser.add_argument("--language", help="Filter by language name")
    parser.add_argument("--all", action="store_true", help="Process all languages (default)")

    args = parser.parse_args()

    try:
        with open(args.filename, "r", encoding="utf-8") as f:
            entries = []
            for line in f:
                line = line.strip()
                if line and ',' in line:
                    language, word = line.split(',', 1)
                    entries.append((language.strip(), word.strip()))
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
        exit(1)

    filter_lang = None if args.all else args.language
    check_encoding(entries, args.encodings, filter_lang)