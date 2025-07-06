#!/opt/homebrew/bin/python3
import sys
import os

def encode_ucs2 (text, encoding):
    # UCS-2 encoding is a fixed-length encoding that uses 2 bytes for each character
    # It can only represent characters in the Basic Multilingual Plane (BMP)
    # UCS-2 is not commonly used anymore, as UTF-16 is more widely adopted
    # However, we can still demonstrate how to encode a string using UCS-2
    if any(ord(c) > 0xFFFF for c in text):
        raise UnicodeEncodeError("ucs-2", text, -1, -1, "Character outside BMP not allowed in UCS-2")
  
    # Use equivalent UTF-16 encoding to simulate UCS-2
    encoding_map = {
        "ucs-2le": "utf-16le",
        "ucs-2be": "utf-16be",
        "ucs-2"   : "utf-16"

    }
    return text.encode(encoding_map[encoding])

def encode_dogs(dogs, encodings):    
    for encoding in encodings:       
        good_dogs = []     
        bad_dogs = []     
        char_count = 0  
        byte_count = 0
        for dog in dogs:        
            try:
                if encoding == "ucs-2" or encoding == "ucs-2le" or encoding == "ucs-2be":
                    encoded_dog = encode_ucs2(dog, encoding)
                else:
                    encoded_dog = dog.encode(encoding)                
                good_dogs.append(dog)
                hex_string = ' '.join(f"{b:02X}" for b in encoded_dog)
                print(f"✅ {encoding + ':':<8} Good {dog} [{hex_string.lower()}] ({len(encoded_dog)} bytes)")                
            except UnicodeEncodeError:                                
                print(f"❌ {encoding + ':':<8} Bad {dog}")                            


def encode_all_dogs(dogs, encoding):    
    good_dogs = []     
    bad_dogs = []     
    char_count = 0  
    byte_count = 0
    for dog in dogs:        
        try:
            if encoding == "ucs-2" or encoding == "ucs-2le" or encoding == "ucs-2be":
                encoded_dog = encode_ucs2(dog, encoding)
            else:
                encoded_dog = dog.encode(encoding)                

            good_dogs.append(dog)
            byte_count += len(encoded_dog)
            char_count += len(dog)
        except UnicodeEncodeError:
            bad_dogs.append(dog)

    bytes_per_char = byte_count / char_count if char_count else 0        
    print(f"✅ {encoding}: {len(good_dogs)} good dogs")        
    print(f"✅ {encoding}: {char_count} chars encoded in {byte_count} bytes, {bytes_per_char:.1f} bytes per char")        
    if bad_dogs:
        print(f"❌ {encoding}: {len(bad_dogs)} bad dogs:")
        for i in range(0, len(bad_dogs), 8):
            print(f"❌ {encoding}: " + '  '.join(bad_dogs[i:i+8]))    


def process_text(texts, encodings, binary=False):    
    good_dogs = []     
    bad_dogs = []     
    char_count = 0  
    byte_count = 0

    for encoding in encodings:
        for text in texts.split(','):
            try:
                if encoding == "ucs-2" or encoding == "ucs-2le" or encoding == "ucs-2be":
                    encoded_text = encode_ucs2(text, encoding)
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
    if not (2 <= len(sys.argv) <= 3):
        print("Usage: encode.py ENCODING1 [ENCODING2] < dogs.txt")
        sys.exit(1)

    enc1 = sys.argv[1]
    enc2 = sys.argv[2] if len(sys.argv) == 3 else None

    if not sys.stdin.isatty():
        dogs = [line.strip() for line in sys.stdin]
        if enc2:
            # comparison mode
            bad1 = set()
            bad2 = set()
            good1 = set()
            good2 = set()

            for dog in dogs:
                try:
                    dog.encode(enc1)
                    good1.add(dog)
                except UnicodeEncodeError:
                    bad1.add(dog)
                try:
                    dog.encode(enc2)
                    good2.add(dog)
                except UnicodeEncodeError:
                    bad2.add(dog)


            byte_count1 = sum(len(dog.encode(enc1)) for dog in good1)
            char_count1 = sum(len(dog) for dog in good1)
            byte_count2 = sum(len(dog.encode(enc2)) for dog in good2)
            char_count2 = sum(len(dog) for dog in good2)

            bad_enc1_good_enc2 = sorted(bad1 & good2)
            good_enc1_bad_enc2 = sorted(good1 & bad2)

            bad_both = sorted(bad1 & bad2)
            good_both = sorted(good1 & good2)
            if good_both:
                print(f"✅ {enc1} ✅ {enc2}: {len(good_both)} dogs")
                for i in range(0, len(good_both), 8):
                    print("  " + "  ".join(good_both[i:i+8]))

            if bad_enc1_good_enc2:
                print(f"❌ {enc1} ✅ {enc2}: {len(bad_enc1_good_enc2)} dogs")
                for i in range(0, len(bad_enc1_good_enc2), 8):
                    print("  " + "  ".join(bad_enc1_good_enc2[i:i+8]))
            if good_enc1_bad_enc2:
                print(f"✅ {enc1} ❌ {enc2}: {len(good_enc1_bad_enc2)} dogs")
                for i in range(0, len(good_enc1_bad_enc2), 8):
                    print("  " + "  ".join(good_enc1_bad_enc2[i:i+8]))

            if bad_both:
                print(f"❌ {enc1} ❌ {enc2}: {len(bad_both)} dogs")
                for i in range(0, len(bad_both), 8):
                    print("  " + "  ".join(bad_both[i:i+8]))

            print(f"\n✅ {enc1}→{enc2}: {len(good_both)}→{len(good_both) + len(bad_enc1_good_enc2)} good dogs")
            print(f"✅ {enc1}: {char_count1} chars encoded in {byte_count1} bytes, {byte_count1 / char_count1:.1f} bytes per char")
            print(f"✅ {enc2}: {char_count2} chars encoded in {byte_count2} bytes, {byte_count2 / char_count2:.1f} bytes per char")
        else:
            # single encoding mode
            good = []
            bad = []
            for dog in dogs:
                try:
                    dog.encode(enc1)
                    good.append(dog)
                except UnicodeEncodeError:
                    bad.append(dog)

            if bad:
                print(f"✅ {enc1}: {len(good)} good dogs")
                for i in range(0, len(good), 8):
                    print("  " + "  ".join(good[i:i+8]))

                print(f"❌ {enc1}: {len(bad)} bad dogs")
                for i in range(0, len(bad), 8):
                    print("  " + "  ".join(bad[i:i+8]))            

                byte_count = sum(len(dog.encode(enc1)) for dog in good)
                char_count = sum(len(dog) for dog in good)
                print(f"{enc1}: {char_count} chars encoded in {byte_count} bytes, {byte_count / char_count:.1f} bytes per char\n")
            else:
                byte_count = sum(len(dog.encode(enc1)) for dog in good)
                char_count = sum(len(dog) for dog in good)
                print(f"✅ {enc1}: {len(good)} good dogs")
                print(f"{enc1}: {char_count} chars encoded in {byte_count} bytes, {byte_count / char_count:.1f} bytes per char")

if __name__ == "__main__":    
    main()