#!/usr/bin/env python3
"""
Day 74 - Flask Database App
Flask application with SQLAlchemy database
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, User, Post
from config import DevelopmentConfig
from datetime import datetime

# Create app
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    users = User.query.all()
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('index.html', 
                          title='Home',
                          users=users,
                          posts=posts,
                          total_users=User.query.count(),
                          total_posts=Post.query.count())


@app.route('/users')
def users():
    """List all users"""
    all_users = User.query.order_by(User.name).all()
    return render_template('users.html', title='Users', users=all_users)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    """Add a new user"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        age = request.form.get('age', '').strip()
        city = request.form.get('city', '').strip()
        
        # Validation
        if not name or not email:
            flash('Name and email are required!', 'error')
            return render_template('add.html', title='Add User')
        
        # Check if email exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash(f'Email {email} already exists!', 'error')
            return render_template('add.html', title='Add User')
        
        # Create user
        user = User(
            name=name,
            email=email,
            age=int(age) if age else None,
            city=city if city else None
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {name} added successfully!', 'success')
        return redirect(url_for('users'))
    
    return render_template('add.html', title='Add User')


@app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit a user"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        age = request.form.get('age', '').strip()
        city = request.form.get('city', '').strip()
        
        if not name or not email:
            flash('Name and email are required!', 'error')
            return render_template('edit.html', title='Edit User', user=user)
        
        # Check email conflict
        existing = User.query.filter(User.email == email, User.id != user_id).first()
        if existing:
            flash(f'Email {email} is already taken!', 'error')
            return render_template('edit.html', title='Edit User', user=user)
        
        # Update user
        user.name = name
        user.email = email
        user.age = int(age) if age else None
        user.city = city if city else None
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash(f'User {name} updated successfully!', 'success')
        return redirect(url_for('users'))
    
    return render_template('edit.html', title='Edit User', user=user)


@app.route('/user/delete/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Delete user's posts first
        Post.query.filter_by(user_id=user_id).delete()
        
        db.session.delete(user)
        db.session.commit()
        
        flash(f'User {user.name} deleted successfully!', 'success')
        return redirect(url_for('users'))
    
    return render_template('delete.html', title='Delete User', user=user)


@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """View user details"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    return render_template('user_detail.html', title='User Detail', user=user, posts=posts)


# ==================== POST ROUTES ====================

@app.route('/posts')
def posts():
    """List all posts"""
    all_posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('posts.html', title='Posts', posts=all_posts)


@app.route('/post/add', methods=['GET', 'POST'])
def add_post():
    """Add a new post"""
    users = User.query.all()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        user_id = request.form.get('user_id', '').strip()
        
        if not title or not content or not user_id:
            flash('Title, content and author are required!', 'error')
            return render_template('add_post.html', title='Add Post', users=users)
        
        post = Post(
            title=title,
            content=content,
            user_id=int(user_id)
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash(f'Post "{title}" added successfully!', 'success')
        return redirect(url_for('posts'))
    
    return render_template('add_post.html', title='Add Post', users=users)


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    """View post details"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', title='Post Detail', post=post)


# ==================== API ROUTES ====================

@app.route('/api/users')
def api_users():
    """API endpoint for users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@app.route('/api/users/<int:user_id>')
def api_user(user_id):
    """API endpoint for single user"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@app.route('/api/posts')
def api_posts():
    """API endpoint for posts"""
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])


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
    return {'now': datetime.now()}


# ==================== MAIN ====================

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
