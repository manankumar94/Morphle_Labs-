from flask import Flask, send_from_directory
import os
import subprocess
import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

full_name = os.getenv("FULL_NAME", "Unknown")

@app.route('/')
def home():
    return "<h2>Welcome! Visit <a href='/htop'>/htop</a> to see system info.</h2>"

@app.route('/favicon.ico')
def favicon():
    return "", 204  

@app.route('/htop')
def show_system_info():
    user_name = os.getenv("USER") or os.getenv("USERNAME") or "Unknown"
    
    ist_timezone = pytz.timezone("Asia/Kolkata")
    server_time = datetime.datetime.now(ist_timezone).strftime("%Y-%m-%d %H:%M:%S %Z")
    
    try:
        system_status = subprocess.check_output("top -b -n 1", shell=True, text=True)
    except Exception as error:
        system_status = f"Error fetching system status: {error}"
    
    return f"""
    <html>
    <head><title>System Info</title></head>
    <body>
        <h2>Name: {full_name}</h2>
        <h3>User: {user_name}</h3>
        <h3>Server Time (IST): {server_time}</h3>
        <h3>System Status:</h3>
        <pre>{system_status}</pre>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
