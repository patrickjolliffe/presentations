#!/usr/bin/env python3
import sys
import os
import argparse

def try_encode(text, encoding):
    try:
        if encoding.lower() == 'ucs-2':
            # Simulate UCS-2: encode as UTF-16-LE, but reject characters outside BMP.
            # Any UnicodeEncodeError (including for characters > U+FFFF) should cause this word to be marked as a bad dog.
            encoded_bytes = text.encode('utf-16-le')
            for ch in text:
                if ord(ch) > 0xFFFF:
                    # UCS-2 cannot encode characters outside the BMP (U+0000 to U+FFFF)
                    raise UnicodeEncodeError("ucs-2", ch, -1, -1, "character outside BMP")
            return True, encoded_bytes
        else:
            encoded_bytes = text.encode(encoding)
            return True, encoded_bytes
    except UnicodeEncodeError:
        return False, None

def process_lines(lines, encoding, filter_language=None, binary=False, show_details=False):
    good_dogs = []
    bad_dogs = []
    total_bytes = 0

    for dog in (line.strip() for line in lines if line.strip()):
        success, encoded = try_encode(dog, encoding)
        if success:
            byte_count = len(encoded)
            if show_details:
                if binary:
                    bin_string = ' '.join(f"{b:08b}" for b in encoded)
                    print(f"Good {dog} [{bin_string}] ({byte_count} bytes)")
                else:
                    hex_string = ' '.join(f"{b:02X}" for b in encoded)
                    print(f"Good {dog} [{hex_string.lower()}] ({byte_count} bytes)")
            good_dogs.append((dog, encoded))
            total_bytes += byte_count
        else:
            if show_details:
                print(f"Bad {dog}")
            bad_dogs.append(dog)

    return good_dogs, bad_dogs, total_bytes

def main():
    parser = argparse.ArgumentParser(description="Check if text can be encoded with a given encoding, and report good and bad dogs.")
    parser.add_argument("encoding", help="Encoding to use (e.g., ascii, utf-8, utf-16)")
    parser.add_argument("--list", action="store_true", help="List good and bad dogs after encoding")
    parser.add_argument("--details", action="store_true", help="Show hex or binary output for each encoded dog")

    parser.add_argument("-f", "--file", help="Text filename to process")
    parser.add_argument("-t", "--text", help="Comma-separated text to process")

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

    good_dogs, bad_dogs, total_bytes = process_lines(lines, args.encoding, None, args.binary, args.details)

    if not args.list and not args.details:
        char_count = sum(len(dog) for dog, _ in good_dogs)
        dog_count = len(good_dogs)
        avg_bytes_per_dog = total_bytes / dog_count if dog_count else 0
        avg_bytes_per_char = total_bytes / char_count if char_count else 0
        print(f"\nSummary of encoding with {args.encoding}")
        print(f"✅  {dog_count} good dogs ({char_count} chars) in {total_bytes} bytes")
        print(f"Average: {avg_bytes_per_dog:.1f} bytes per dog, {avg_bytes_per_char:.1f} bytes per char")
        if bad_dogs:
            print(f"❌  {len(bad_dogs)} bad dogs:")
            for i in range(0, len(bad_dogs), 10):
                print('  ' + '  '.join(bad_dogs[i:i+10]))
        else:
            print("✅  0 bad dogs")

if __name__ == "__main__":
    main()