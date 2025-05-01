# Hack-Lab: Web Penetration Testing Simulator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Hack-Lab is an educational tool designed to help security enthusiasts and developers understand common web vulnerabilities through a practical, hands-on approach. This project simulates vulnerable web applications with a controlled environment to practice ethical hacking techniques.

## 🔍 Features

The simulator includes the following vulnerabilities:

- **SQL Injection**: Practice breaking SQL query integrity
- **Cross-Site Scripting (XSS)**: Experiment with inserting malicious scripts
- **File Upload Bypass**: Test file upload security controls
- **Command Injection**: Exploit vulnerable command execution
- **Path Traversal**: Access unauthorized files on the server
- **Cross-Site Request Forgery (CSRF)**: Execute unwanted actions on behalf of users

## 📋 Components

- **Vulnerable Flask App**: A deliberately insecure web application
- **Attack Tools**: Python scripts to demonstrate exploits
- **Terminal GUI**: Easy-to-use terminal interface for controlling the lab

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hack-lab.git
   cd hack-lab
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Option 1: Terminal GUI

1. Launch the terminal interface:
   ```bash
   python terminal_gui.py
   ```

2. Use the menu to start the server and run various attack tools.

### Option 2: Manual Execution

1. Start the vulnerable server:
   ```bash
   python app.py
   ```

2. Run individual attack tools:
   ```bash
   python tool_sqli.py    # SQL Injection test
   python tool_xss.py     # XSS test
   python tool_upload.py  # File upload bypass test
   python tool_command.py # Command Injection test
   python tool_traversal.py # Path Traversal test
   python tool_csrf.py    # CSRF test
   ```

3. Access the web interface at [http://localhost:5000](http://localhost:5000)

## 💻 Vulnerable Endpoints

- **SQL Injection**: [http://localhost:5000/sqli](http://localhost:5000/sqli)
- **XSS**: [http://localhost:5000/xss](http://localhost:5000/xss)
- **Upload Bypass**: [http://localhost:5000/upload](http://localhost:5000/upload)
- **Command Injection**: [http://localhost:5000/command](http://localhost:5000/command)
- **Path Traversal**: [http://localhost:5000/traversal](http://localhost:5000/traversal)
- **CSRF**: [http://localhost:5000/csrf](http://localhost:5000/csrf)

## ⚠️ Disclaimer

This project is designed for educational purposes only. The vulnerabilities are intentional for learning about web security. Never use these techniques against systems without explicit permission. Always practice ethical hacking.

## 🔒 Security Tips

For each vulnerability demonstrated, the README includes mitigation strategies:

### SQL Injection Prevention
- Use parameterized queries
- Implement input validation
- Apply the principle of least privilege for database users

### XSS Prevention
- Sanitize user input
- Implement Content Security Policy (CSP)
- Use frameworks that automatically escape output

### File Upload Security
- Validate file extensions and content types
- Scan uploads for malware
- Store uploads outside the web root

### Command Injection Prevention
- Avoid using system commands with user input
- Implement strict input validation and whitelisting
- Use libraries that handle command execution safely

### Path Traversal Prevention
- Validate and sanitize file paths
- Use path canonicalization
- Implement proper access controls

### CSRF Prevention
- Implement anti-CSRF tokens
- Use SameSite cookie attribute
- Verify the Origin/Referer header

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
