import requests
import os

url = "http://localhost:5000/upload"

filename = "test.php"
with open(filename, "w") as f:
    f.write("<?php echo 'uploaded'; ?>")

files = {"file": (filename, open(filename, "rb"), "application/x-php")}
print("[+] Uploading file...")
r = requests.post(url, files=files)
print("Response:", r.text)

# Clean up
os.remove(filename)
