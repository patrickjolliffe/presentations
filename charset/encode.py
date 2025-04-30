#!/usr/bin/env python3
import sys
import os
import argparse

def try_encode(text, encoding):
    try:
        encoded_bytes = text.encode(encoding)
        return True, encoded_bytes
    except Exception:
        return False, None

def process_lines(lines, encoding, filter_language=None, binary=False, show_details=False):
    good_dogs = []
    bad_dogs = []
    total_bytes = 0

    prefix = f"{filter_language}({encoding})" if filter_language else encoding

    for line in lines:
        line = line.strip()
        if not line or ',' not in line:
            continue
        language, dog = line.split(',', 1)
        language = language.strip()
        dog = dog.strip()

        if filter_language and language.lower() != filter_language.lower():
            continue

        success, encoded = try_encode(dog, encoding)
        if success:
            byte_count = len(encoded)
            if show_details or filter_language:
                if binary:
                    bin_string = ' '.join(f"{b:08b}" for b in encoded)
                    print(f"Good {dog} [{bin_string}] ({byte_count} bytes)")
                else:
                    hex_string = ' '.join(f"{b:02X}" for b in encoded)
                    print(f"Good {dog} [{hex_string.lower()}] ({byte_count} bytes)")
            good_dogs.append((dog, encoded))
            total_bytes += byte_count
        else:
            if show_details or filter_language:
                print(f"Bad {dog}")
            bad_dogs.append(dog)

    return good_dogs, bad_dogs, total_bytes

def main():
    parser = argparse.ArgumentParser(description="Check if CSV fields or text can be encoded with a given encoding, and report good and bad dogs.")
    parser.add_argument("encoding", help="Encoding to use (e.g., ascii, utf-8, utf-16)")
    parser.add_argument("--list", action="store_true", help="List good and bad dogs after encoding")
    parser.add_argument("--details", action="store_true", help="Show hex or binary output for each encoded dog")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="CSV filename to process")
    group.add_argument("-t", "--text", help="Comma-separated text to process")

    parser.add_argument("--language", help="Language label to use in output", default=None)
    parser.add_argument("--binary", action="store_true", help="Output in binary instead of hexadecimal")

    args = parser.parse_args()

    if args.file:
        if not os.path.isfile(args.file):
            print(f"File not found: {args.file}")
            sys.exit(1)
        with open(args.file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    elif args.text:
        pieces = [piece.strip() for piece in args.text.split(',')]
        good = []
        bad = []

        for piece in pieces:
            if not piece:
                continue
            success, encoded = try_encode(piece, args.encoding)
            if success:
                if args.binary:
                    bin_string = ' '.join(f"{b:08b}" for b in encoded)
                    print(f'"{piece}" encoded in {args.encoding} is [{bin_string}]')
                else:
                    hex_string = ' '.join(f"{b:02X}" for b in encoded)
                    print(f'"{piece}" encoded in {args.encoding} is [{hex_string}]')
                good.append(piece)
            else:
                print(f'{args.encoding}: Unable to encode "{piece}"')
                bad.append(piece)

        if args.list and (good or bad):
            print()
            if good:
                print("Encoded:")
                for item in good:
                    print(f"  {item}")
            if bad:
                print("Unencoded:")
                for item in bad:
                    print(f"  {item}")

        sys.exit(0)
    else:
        print("Either --file or --text must be provided.")
        sys.exit(1)

    filter_lang = args.language or None
    good_dogs, bad_dogs, total_bytes = process_lines(lines, args.encoding, filter_lang, args.binary, args.details)

    prefix = f"{args.language}({args.encoding})" if args.language else args.encoding

    if not args.language:
        average = total_bytes / len(good_dogs) if good_dogs else 0
        print(f"\nSummary of encoding with {args.encoding}")
        print(f"{len(good_dogs)} good dogs in {total_bytes} bytes (average {average:.1f} bytes)")
        print(f"{len(bad_dogs)} bad dogs")

if __name__ == "__main__":
    main()