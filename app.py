from flask import Flask, request, render_template_string, redirect, send_from_directory, jsonify
import os
import json
import importlib

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return """
    <h2>Hack-Lab Demo</h2>
    <ul>
        <li><a href='/sqli'>SQL Injection Form</a></li>
        <li><a href='/xss'>XSS Test</a></li>
        <li><a href='/upload'>Upload Bypass</a></li>
        <li><a href='/command'>Command Injection</a></li>
        <li><a href='/traversal'>Path Traversal</a></li>
        <li><a href='/csrf'>CSRF Vulnerability</a></li>
        <li><a href='/recon'>Reconnaissance</a></li>
    </ul>
    """

@app.route("/sqli", methods=["GET", "POST"])
def sqli():
    result = ""
    if request.method == "POST":
        username = request.form['username']
        query = f"SELECT * FROM users WHERE username = '{username}'"
        result = f"Query Executed: {query}"
    return f"""
    <h3>SQL Injection Demo</h3>
    <form method='POST'>
        Username: <input name='username'>
        <button type='submit'>Submit</button>
    </form>
    <p>{result}</p>
    """

@app.route("/xss", methods=["GET", "POST"])
def xss():
    comment = ""
    if request.method == "POST":
        comment = request.form['comment']
    return render_template_string(f"""
    <h3>XSS Demo</h3>
    <form method='POST'>
        Comment: <input name='comment'>
        <button type='submit'>Submit</button>
    </form>
    <p>Output: {comment}</p>
    """)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    message = ""
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        message = "Uploaded successfully"
    return f"""
    <h3>Upload Bypass</h3>
    <form method='POST' enctype='multipart/form-data'>
        File: <input type='file' name='file'>
        <button type='submit'>Upload</button>
    </form>
    <p>{message}</p>
    """

@app.route("/command", methods=["GET", "POST"])
def command_injection():
    output = ""
    if request.method == "POST":
        ip = request.form['ip']
        # Vulnerable command injection
        cmd = f"ping -c 1 {ip}"
        try:
            output = os.popen(cmd).read()
        except:
            output = "Error executing command"
    return f"""
    <h3>Command Injection Demo</h3>
    <form method='POST'>
        IP to ping: <input name='ip' placeholder="8.8.8.8">
        <button type='submit'>Ping</button>
    </form>
    <pre>{output}</pre>
    """

@app.route("/traversal", methods=["GET"])
def path_traversal():
    file = request.args.get('file', 'safe.txt')
    try:
        # Vulnerable path traversal
        with open(file, 'r') as f:
            content = f.read()
    except:
        content = f"Error: Could not read file {file}"
    return f"""
    <h3>Path Traversal Demo</h3>
    <p>Current file: {file}</p>
    <p>Content:</p>
    <pre>{content}</pre>
    <p>Try to access another file using the 'file' parameter.</p>
    """

@app.route("/csrf", methods=["GET", "POST"])
def csrf():
    message = ""
    action = ""
    if request.method == "POST":
        action = request.form.get('action', '')
        if action == "transfer":
            amount = request.form.get('amount', '0')
            to = request.form.get('to', 'nobody')
            message = f"Transferred ${amount} to {to}"
    return f"""
    <h3>CSRF Vulnerability Demo</h3>
    <form method='POST'>
        <input type='hidden' name='action' value='transfer'>
        Amount: <input name='amount' type='number' value='100'>
        To Account: <input name='to' value='friend'>
        <button type='submit'>Transfer</button>
    </form>
    <p>{message}</p>
    """

@app.route("/recon", methods=["GET", "POST"])
def recon():
    result = ""
    if request.method == "POST":
        domain = request.form['domain']
        osint_framework = importlib.import_module('tool_osint').OSINTFramework()
        
        # For the web UI, we'll do a simplified scan to avoid long waits
        try:
            # Do basic lookups
            whois_data = osint_framework.whois_lookup(domain)
            ip = osint_framework.dns_lookup(domain)
            
            # Format result
            result = f"<h4>Results for {domain}</h4>"
            result += f"<p><strong>IP Address:</strong> {ip}</p>"
            
            if whois_data:
                result += "<p><strong>WHOIS Data:</strong></p>"
                result += "<ul>"
                if hasattr(whois_data, 'registrar'):
                    result += f"<li>Registrar: {whois_data.registrar}</li>"
                if hasattr(whois_data, 'creation_date'):
                    result += f"<li>Creation Date: {whois_data.creation_date}</li>"
                if hasattr(whois_data, 'expiration_date'):
                    result += f"<li>Expiration Date: {whois_data.expiration_date}</li>"
                result += "</ul>"
            
            # Scan a few ports
            if ip:
                open_ports = osint_framework.port_scan(ip, [80, 443, 22, 21, 25])
                if open_ports:
                    result += "<p><strong>Open Ports:</strong></p>"
                    result += "<ul>"
                    for port in open_ports:
                        result += f"<li>Port {port}</li>"
                    result += "</ul>"
        
        except Exception as e:
            result = f"<p>Error during analysis: {str(e)}</p>"
    
    return f"""
    <h3>OSINT Tool</h3>
    <form method='POST'>
        Domain: <input name='domain' placeholder="example.com">
        <button type='submit'>Run Analysis</button>
    </form>
    <div>{result}</div>
    <p><i>For full intelligence gathering capabilities, use the terminal_gui.py or tool_osint.py directly.</i></p>
    """

@app.route("/uploads/<filename>")
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
