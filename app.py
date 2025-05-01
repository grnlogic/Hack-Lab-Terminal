from flask import Flask, request, render_template_string, redirect, send_from_directory
import os

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

@app.route("/uploads/<filename>")
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
