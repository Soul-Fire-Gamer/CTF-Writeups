from PIL import Image

def decrypt_hidden_flag(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    width, height = img.size
    
    extracted_nibbles = []
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            if b <= 15:
                extracted_nibbles.append(b)
                
    print(f"Found {len(extracted_nibbles)} corrupted pixels containing hidden data.")
    
    decoded_bytes = bytearray()
    
    for i in range(0, len(extracted_nibbles) - 1, 2):
        high_nibble = extracted_nibbles[i]
        low_nibble = extracted_nibbles[i+1]
        
        full_byte = (high_nibble << 4) | low_nibble
        decoded_bytes.append(full_byte)
        
    print("\n--- Decoded Flag Output ---")
    try:
        flag_text = decoded_bytes.decode('utf-8', errors='ignore')
        print(flag_text)
    except Exception as e:
        print(f"Could not decode as text. Raw bytes: {list(decoded_bytes)}")

decrypt_hidden_flag("/Users/kennethxie/Downloads/corrupt4.png")