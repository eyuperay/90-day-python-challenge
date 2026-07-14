#!/usr/bin/env python3
"""
Day 73 - Flask Web App
Simple web application using Flask
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Sample data
users = [
    {'id': 1, 'name': 'Ahmet Yilmaz', 'email': 'ahmet@email.com'},
    {'id': 2, 'name': 'Mehmet Demir', 'email': 'mehmet@email.com'},
    {'id': 3, 'name': 'Ayse Kaya', 'email': 'ayse@email.com'}
]

messages = []


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    now = datetime.datetime.now()
    return render_template('index.html', 
                          title='Home', 
                          year=now.year,
                          users=users[:3])


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', title='About')


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    """Hello page"""
    return render_template('hello.html', 
                          title='Hello',
                          name=name)


@app.route('/users')
def list_users():
    """List all users"""
    return render_template('users.html', 
                          title='Users',
                          users=users)


@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """User detail page"""
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return render_template('user_detail.html', 
                              title='User Detail',
                              user=user)
    return "User not found", 404


# ==================== FORM ROUTES ====================

@app.route('/form', methods=['GET', 'POST'])
def form_demo():
    """Form demo page"""
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')
        
        # Save message
        messages.append({
            'name': name,
            'email': email,
            'message': message,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        return render_template('form_result.html',
                              title='Form Result',
                              name=name,
                              email=email,
                              message=message)
    
    return render_template('form.html', title='Contact Form')


# ==================== API ROUTES ====================

@app.route('/api/users')
def api_users():
    """API endpoint for users"""
    return jsonify(users)


@app.route('/api/messages')
def api_messages():
    """API endpoint for messages"""
    return jsonify(messages)


@app.route('/api/time')
def api_time():
    """API endpoint for current time"""
    return jsonify({
        'time': datetime.datetime.now().isoformat(),
        'timestamp': datetime.datetime.now().timestamp()
    })


# ==================== SESSION ROUTES ====================

@app.route('/session/set')
def session_set():
    """Set session variable"""
    session['username'] = 'Guest'
    session['visit_count'] = session.get('visit_count', 0) + 1
    return redirect(url_for('index'))


@app.route('/session/clear')
def session_clear():
    """Clear session"""
    session.clear()
    return redirect(url_for('index'))


# ==================== ERROR HANDLING ====================

@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('404.html', title='Page Not Found'), 404


@app.errorhandler(500)
def internal_error(e):
    """500 error handler"""
    return render_template('500.html', title='Server Error'), 500


# ==================== CONTEXT PROCESSOR ====================

@app.context_processor
def inject_now():
    """Inject current time into all templates"""
    return {'now': datetime.datetime.now()}


# ==================== MAIN ====================

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
