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

@app.route("/uploads/<filename>")
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
