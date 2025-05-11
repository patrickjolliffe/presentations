#!/opt/homebrew/bin/python3
import sys
import os
import argparse

def process_dogs(dogs, encoding, binary=False, show_details=False):    
    good_dogs = []     
    bad_dogs = []     
    char_count = 0  
    byte_count = 0
    for dog in dogs:        
        try:
            encoded_dog = dog.encode(encoding)
            good_dogs.append(dog)
            if show_details:
                if binary:
                    bin_string = ' '.join(f"{b:08b}" for b in encoded_dog)
                    print(f"✅ {encoding + ':':<8} Good {dog} [{bin_string}] ({len(encoded_dog)} bytes)")
                else:
                    hex_string = ' '.join(f"{b:02X}" for b in encoded_dog)
                    print(f"✅ {encoding + ':':<8} Good {dog} [{hex_string.lower()}] ({len(encoded_dog)} bytes)")

            byte_count += len(encoded_dog)
            char_count += len(dog)
        except UnicodeEncodeError:
            bad_dogs.append(dog)
            if show_details:                
                print(f"❌ {encoding + ':':<16} Bad {dog}")                    

    if  not show_details:   
        bytes_per_char = byte_count / char_count if char_count else 0        
        print(f"✅ {encoding}: {len(good_dogs)} good dogs, {char_count} chars in {byte_count} bytes, {bytes_per_char:.1f} bytes per char")        
        if bad_dogs:
            print(f"❌ {encoding}: {len(bad_dogs)} bad dogs")
            for i in range(0, len(bad_dogs), 10):
                print(f"❌ {encoding}: " + '  '.join(bad_dogs[i:i+10]))
        else:
            print("✅  No bad dogs")

def main():
    parser = argparse.ArgumentParser(description="Check if text can be encoded with a given encoding, and report good and bad dogs.")
    parser.add_argument("encodings", help="Comma-separated of encodings (e.g., ascii, utf-8, utf-16)")
    parser.add_argument("--list", action="store_true", help="List good and bad dogs after encoding")
    parser.add_argument("--details", action="store_true", help="Show hex or binary output for each encoded dog")

    parser.add_argument("-f", "--file", help="Text filename to process")
    parser.add_argument("-t", "--text", help="Comma-separated text to process")    

    parser.add_argument("--binary", action="store_true", help="Output in binary instead of hexadecimal")

    args = parser.parse_args()

    if args.file:
        show_details = False
        if not os.path.isfile(args.file):
            print(f"File not found: {args.file}")
            sys.exit(1)
        with open(args.file, 'r', encoding='utf-8') as f:            
            dogs = [line.strip() for line in f]
    elif args.text:
        dogs = [dog.strip() for dog in args.text.split(',')]        
        show_details = True
    else:
        print("Either --file or --text must be provided.")
        sys.exit(1)

    for encoding in args.encodings.split(','):
        process_dogs(dogs, encoding, args.binary, show_details)

if __name__ == "__main__":
    main()