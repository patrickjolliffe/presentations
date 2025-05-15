#!/opt/homebrew/bin/python3
import sys
import os
import argparse


def encode_ucs2 (text):
    # UCS-2 encoding is a fixed-length encoding that uses 2 bytes for each character
    # It can only represent characters in the Basic Multilingual Plane (BMP)
    # UCS-2 is not commonly used anymore, as UTF-16 is more widely adopted
    # However, we can still demonstrate how to encode a string using UCS-2
    for c in text:
        if ord(c) > 0xFFFF:
            raise UnicodeEncodeError("ucs-2", text, text.index(c), text.index(c) + 1,
                                     f"character {repr(c)} not in BMP")
    return text.encode("utf-16le")


def process_dogs(dogs, encodings, binary=False, show_details=False):    
    for encoding in encodings:       
        good_dogs = []     
        bad_dogs = []     
        char_count = 0  
        byte_count = 0
        for dog in dogs:        
            try:
                if encoding == "ucs-2":
                    encoded_dog = encode_ucs2(dog)
                else:
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
            print(f"✅ {encoding}: {len(good_dogs)} good dogs")        
            print(f"✅ {encoding}: Encoded {char_count} chars in {byte_count} bytes, {bytes_per_char:.1f} bytes per char")        
            if bad_dogs:
                print(f"❌ {encoding}: {len(bad_dogs)} bad dogs")
                for i in range(0, len(bad_dogs), 8):
                    print(f"❌ {encoding}: " + '  '.join(bad_dogs[i:i+8]))
            else:
                print("✅  No bad dogs")


def process_text(texts, encodings, binary=False):    
    good_dogs = []     
    bad_dogs = []     
    char_count = 0  
    byte_count = 0

    for encoding in encodings:
        for text in texts.split(','):
            try:
                if encoding == "ucs-2":
                    encoded_text = encode_ucs2(text)
                else:
                    encoded_text = text.encode(encoding)                
                if binary:
                    bin_string = ' '.join(f"{b:08b}" for b in encoded_text)
                    print(f"✅ {encoding + ':':<8} \"{text}\"=[{bin_string}]")
                else:
                    hex_string = ' '.join(f"{b:02X}" for b in encoded_text)
                    print(f"✅ {encoding + ':':<8} \"{text}\"=[{hex_string.lower()}]")
            except UnicodeEncodeError:
                print(f"❌ {encoding}: Failed to encode {text}")

def main():
    parser = argparse.ArgumentParser(description="Check if text can be encoded with a given encoding, and report good and bad dogs.")
    parser.add_argument("encodings", help="Comma-separated of encodings (e.g., ascii, utf-8, utf-16)")
    parser.add_argument("--list", action="store_true", help="List good and bad dogs after encoding")
    parser.add_argument("--details", action="store_true", help="Show hex or binary output for each encoded dog")

    parser.add_argument("-f", "--file", action="store_true", help="Process dogs.txt")
    parser.add_argument("-d", "--dogs", help="Comma-separated dogs to process")   
    parser.add_argument("-t", "--text", help="Text to process")    

    parser.add_argument("--binary", action="store_true", help="Output in binary instead of hexadecimal")

    args = parser.parse_args()

    encodings = args.encodings.split(',')        

    if args.text:        
        process_text(args.text, encodings, args.binary)
        sys.exit(1)
    elif args.file:
        show_details = False
        with open("dogs.txt", 'r', encoding='utf-8') as f:            
            dogs = [line.strip() for line in f]
    elif args.dogs:
        dogs = [dog.strip() for dog in args.dogs.split(',')]        
        show_details = True
    else:
        print("Either --file or --text must be provided.")
        sys.exit(1)


    process_dogs(dogs, encodings, args.binary, show_details)

if __name__ == "__main__":
    main()