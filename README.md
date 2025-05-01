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
- **Password Analysis**: Test password strength against cracking attempts
- **Web Reconnaissance**: Gather information about domains and websites

## 📸 Screenshots

### Startup Screen

![Hack-Lab Startup Screen](https://i.ibb.co/dwZbYBPz/Screenshot-from-2025-05-01-23-35-16.png)
_The initial terminal interface when launching Hack-Lab_

### Main Menu

![Hack-Lab Main Menu](https://i.ibb.co/hR84jjfB/Screenshot-from-2025-05-01-23-35-28.png)
_The main menu showing all available tools_

## 📋 Components

- **Vulnerable Flask App**: A deliberately insecure web application
- **Attack Tools**: Python scripts to demonstrate exploits
- **Terminal GUI**: Easy-to-use terminal interface for controlling the lab
- **Password Strength Analyzer**: Tool to evaluate password security
- **Reconnaissance Framework**: Tools for gathering OSINT on websites

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- pip (Python package manager)

### Installation

1. Clone the repository

   ```
   git clone https://github.com/yourusername/Hack-lab.git
   cd Hack-lab
   ```

2. Install dependencies

   ```
   pip install -r requirements.txt
   ```

3. Run the terminal interface
   ```
   python terminal_gui.py
   ```

## 🔒 Security Tips

### SQL Injection Prevention

- Use parameterized queries
- Implement input validation
- Apply the principle of least privilege for database accounts

### XSS Prevention

- Sanitize and validate all user inputs
- Implement Content Security Policy (CSP)
- Use modern frameworks that automatically escape output

### File Upload Security

- Validate file extensions and content types
- Scan uploaded files for malware
- Store uploads outside the web root

### Command Injection Defense

- Avoid using shell commands with user input
- Implement strict input validation
- Use safer alternatives to shell commands

### Path Traversal Protection

- Normalize file paths before use
- Implement proper access controls
- Use safe APIs for file operations

### CSRF Protection

- Implement anti-CSRF tokens
- Use SameSite cookie attribute
- Verify Origin and Referer headers

### Password Security

- Enforce strong password policies
- Use secure password hashing (bcrypt, Argon2)
- Implement multi-factor authentication

### Reconnaissance Best Practices

- Obtain proper authorization before performing reconnaissance on any system
- Document all findings and maintain a clear audit trail
- Use proxies or VPNs when appropriate to protect your identity
- Be aware of and comply with relevant laws and regulations
- Limit the scope of your reconnaissance to avoid disrupting services

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Made with ❤️ by grnlogic
- All the open-source tools that inspired this project
