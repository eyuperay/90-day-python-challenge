#!/usr/bin/env python3
"""
Simple Flask App for Docker Demo
"""

from flask import Flask, jsonify, render_template_string
import datetime
import os
import socket

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Docker Python App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f4f6f9;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #2c3e50; }
        .info { background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .status { color: #27ae60; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐳 Docker Python App</h1>
        <div class="info">
            <p><strong>Status:</strong> <span class="status">Running</span></p>
            <p><strong>Container:</strong> {{ container_id }}</p>
            <p><strong>Hostname:</strong> {{ hostname }}</p>
            <p><strong>Time:</strong> {{ time }}</p>
            <p><strong>Python Version:</strong> {{ python_version }}</p>
        </div>
        <p>This app is running inside a Docker container!</p>
        <p>API Endpoints:</p>
        <ul>
            <li><a href="/api/health">/api/health</a> - Health check</li>
            <li><a href="/api/info">/api/info</a> - Container info</li>
            <li><a href="/api/time">/api/time</a> - Current time</li>
        </ul>
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    """Home page"""
    return render_template_string(
        HTML_TEMPLATE,
        container_id=socket.gethostname(),
        hostname=os.getenv('HOSTNAME', 'localhost'),
        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        python_version=os.sys.version
    )


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    })


@app.route('/api/info')
def info():
    """Container info endpoint"""
    return jsonify({
        'container_id': socket.gethostname(),
        'hostname': os.getenv('HOSTNAME', 'unknown'),
        'python_version': os.sys.version,
        'working_dir': os.getcwd(),
        'environment': dict(os.environ)
    })


@app.route('/api/time')
def current_time():
    """Current time endpoint"""
    return jsonify({
        'time': datetime.datetime.now().isoformat(),
        'timestamp': datetime.datetime.now().timestamp()
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
