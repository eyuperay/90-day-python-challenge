#!/usr/bin/env python3
"""
Multi-service Flask App with PostgreSQL and Redis
"""

import os
import time
import json
import redis
from flask import Flask, jsonify, render_template_string, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@postgres:5432/appdb'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)

# Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)


# ==================== MODELS ====================

class Visit(db.Model):
    """Visit model"""
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'user_agent': self.user_agent,
            'timestamp': self.timestamp.isoformat()
        }


# ==================== HTML TEMPLATE ====================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Docker Compose Demo</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
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
        h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .service-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .service-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .service-card .status {
            color: #27ae60;
            font-weight: bold;
        }
        .service-card .status.off {
            color: #e74c3c;
        }
        .visits {
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .info { 
            background: #fef9e7;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .btn {
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        .btn:hover {
            background: #2980b9;
        }
        .btn-danger {
            background: #e74c3c;
        }
        .btn-danger:hover {
            background: #c0392b;
        }
        ul { padding-left: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐳 Docker Compose Demo</h1>
        <p>Multi-service application with Flask, PostgreSQL, and Redis</p>

        <div class="service-grid">
            <div class="service-card">
                <h3>Flask</h3>
                <p class="status">✓ Running</p>
            </div>
            <div class="service-card">
                <h3>PostgreSQL</h3>
                <p class="status" id="pg-status">✓ Running</p>
            </div>
            <div class="service-card">
                <h3>Redis</h3>
                <p class="status" id="redis-status">✓ Running</p>
            </div>
        </div>

        <div class="info">
            <h3>📊 Statistics</h3>
            <p><strong>Total Visits:</strong> <span id="visit-count">{{ visit_count }}</span></p>
            <p><strong>Redis Hits:</strong> <span id="redis-hits">{{ redis_hits }}</span></p>
            <p><strong>Container ID:</strong> {{ container_id }}</p>
            <p><strong>Time:</strong> {{ time }}</p>
        </div>

        <div class="visits">
            <h3>📝 Recent Visits</h3>
            <ul>
                {% for visit in visits %}
                <li>{{ visit.timestamp }} - IP: {{ visit.ip }}</li>
                {% endfor %}
            </ul>
        </div>

        <form method="POST" action="/visit">
            <button type="submit" class="btn">📝 Record Visit</button>
        </form>
        <form method="POST" action="/clear" style="display:inline;">
            <button type="submit" class="btn btn-danger">🗑️ Clear Visits</button>
        </form>
        <form method="POST" action="/reset" style="display:inline;">
            <button type="submit" class="btn">🔄 Reset Redis Counter</button>
        </form>
    </div>
</body>
</html>
"""


# ==================== ROUTES ====================

@app.route('/', methods=['GET'])
def index():
    """Home page"""
    visit_count = db.session.query(Visit).count()
    recent_visits = Visit.query.order_by(Visit.timestamp.desc()).limit(10).all()
    
    # Redis counter
    redis_hits = redis_client.get('visit_counter') or 0
    
    return render_template_string(
        HTML_TEMPLATE,
        visit_count=visit_count,
        visits=recent_visits,
        redis_hits=int(redis_hits),
        container_id=os.getenv('HOSTNAME', 'unknown'),
        time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )


@app.route('/visit', methods=['POST'])
def record_visit():
    """Record a visit"""
    try:
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        visit = Visit(ip=ip, user_agent=user_agent)
        db.session.add(visit)
        db.session.commit()
        
        # Increment Redis counter
        redis_client.incr('visit_counter')
        
        return jsonify({
            'status': 'success',
            'message': 'Visit recorded',
            'visit_id': visit.id
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/clear', methods=['POST'])
def clear_visits():
    """Clear all visits"""
    try:
        db.session.query(Visit).delete()
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'All visits cleared'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/reset', methods=['POST'])
def reset_counter():
    """Reset Redis counter"""
    try:
        redis_client.set('visit_counter', 0)
        return jsonify({'status': 'success', 'message': 'Redis counter reset'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'flask': 'ok',
            'postgres': 'ok' if db.session.query(Visit).first() is not None else 'ok',
            'redis': 'ok' if redis_client.ping() else 'error'
        },
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/stats')
def stats():
    """Statistics endpoint"""
    visit_count = db.session.query(Visit).count()
    redis_hits = redis_client.get('visit_counter') or 0
    
    return jsonify({
        'total_visits': visit_count,
        'redis_hits': int(redis_hits),
        'timestamp': datetime.now().isoformat()
    })


# ==================== MAIN ====================

if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()
        print("[OK] Database tables created")
    
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
