#!/opt/homebrew/bin/python3
import sys
import os
import argparse

def try_encode(text, encoding, binary=False, show_details=False):    
    encoded_bytes = text.encode(encoding)
    if show_details:
        if binary:
            bin_string = ' '.join(f"{b:08b}" for b in encoded_bytes)
            print(f"Good {text} [{bin_string}] ({len(encoded_bytes)} bytes)")
        else:
            hex_string = ' '.join(f"{b:02X}" for b in encoded_bytes)
            print(f"Good {text} [{hex_string.lower()}] ({len(encoded_bytes)} bytes)")

    return encoded_bytes
    

def process_dogs(dogs, encoding, binary=False, show_details=False):
    good_byte_count = 0
    good_dog_count = 0
    good_char_count = 0
    bad_dogs = []    
    good_dogs = []    
    
    for dog in dogs:
        try:
            encoded_dog = try_encode(dog, encoding, binary, show_details)   
            good_byte_count += len(encoded_dog)
            good_char_count += len(dog)
            good_dog_count += 1
        except UnicodeEncodeError:
            if show_details:
                print(f"Bad {dog}")
            bad_dogs.append(dog)

    return good_dog_count, bad_dogs, good_char_count, good_byte_count

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
            dogs = f.readlines()
    elif args.text:
        dogs = [dog.strip() for dog in args.text.split(',')]
        


    else:
        print("Either --file or --text must be provided.")
        sys.exit(1)
        
    good = []
    bad = []        
    good_dog_count, bad_dogs, good_char_count, good_byte_count = process_dogs(dogs, args.encoding, args.binary, args.details)

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


    if not args.list and not args.details:               
        avg_bytes_per_dog = good_byte_count / good_dog_count if good_dog_count else 0
        avg_bytes_per_char = good_byte_count / good_char_count if good_char_count else 0
        print(f"Summary of encoding with {args.encoding}")
        print(f"✅  {good_dog_count} good dogs ({good_char_count} chars) in {good_byte_count} bytes")
        print(f"Average: {avg_bytes_per_dog:.1f} bytes per dog, {avg_bytes_per_char:.1f} bytes per char")
        if bad_dogs:
            print(f"❌  {len(bad_dogs)} bad dogs:")
            for i in range(0, len(bad_dogs), 10):
                print('  ' + '  '.join(bad_dogs[i:i+10]))
        else:
            print("✅  0 bad dogs")

if __name__ == "__main__":
    main()