"""
Simple Flask App for CI/CD Demo
"""

from flask import Flask, jsonify, render_template_string
import datetime
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CI/CD Demo</title>
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
        .status { color: #27ae60; font-weight: bold; }
        .info { background: #e8f4fd; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 CI/CD Demo App</h1>
        <div class="info">
            <p><strong>Status:</strong> <span class="status">Running</span></p>
            <p><strong>Version:</strong> {{ version }}</p>
            <p><strong>Environment:</strong> {{ environment }}</p>
            <p><strong>Time:</strong> {{ time }}</p>
        </div>
        <p>This app is deployed via GitHub Actions!</p>
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    """Home page"""
    return render_template_string(
        HTML_TEMPLATE,
        version=os.getenv('APP_VERSION', '1.0.0'),
        environment=os.getenv('APP_ENV', 'development'),
        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'timestamp': datetime.datetime.now().isoformat()
    })


@app.route('/api/info')
def info():
    """Info endpoint"""
    return jsonify({
        'app': 'CI/CD Demo',
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'environment': os.getenv('APP_ENV', 'development'),
        'python_version': os.sys.version
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
