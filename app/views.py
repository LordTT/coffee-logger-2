"""
Views/Controllers for Coffee Logger Application
"""

from app import app, db
from app.models import User, CoffeeType, CoffeeLog
from flask import render_template, request, redirect, url_for, jsonify, session
import json
import hashlib


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password for comparison (in a real app, use proper password hashing)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if user and user.id:  # Simplified check - in real app, compare hashed passwords
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error='Username already exists')
        
        # Create new user (hash password in real app)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/logs')
def logs():
    """Logs page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('logs.html')


@app.route('/coffee-types')
def coffee_types():
    """Coffee types page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('coffee_types.html')


@app.route('/profile')
def profile():
    """User profile page"""

    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')


# API Routes

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    } for user in users])


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})


@app.route('/api/user', methods=['GET'])
def get_current_user():
    """Get current logged-in user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'created_at': user.created_at.isoformat()
    })


@app.route('/api/coffee-types', methods=['GET'])
def get_coffee_types():
    """Get all coffee types"""
    coffee_types = CoffeeType.query.all()
    return jsonify([{
        'id': ct.id,
        'name': ct.name,
        'description': ct.description,
        'user_id': ct.user_id,
        'created_at': ct.created_at.isoformat()
    } for ct in coffee_types])


@app.route('/api/coffee-types', methods=['POST'])
def create_coffee_type():
    """Create a new coffee type"""
    data = request.get_json()
    coffee_type = CoffeeType(
        name=data['name'],
        description=data.get('description', ''),
        user_id=data['user_id']
    )
    db.session.add(coffee_type)
    db.session.commit()
    return jsonify({
        'id': coffee_type.id,
        'name': coffee_type.name,
        'description': coffee_type.description,
        'user_id': coffee_type.user_id
    })


@app.route('/api/coffee-logs', methods=['GET'])
def get_coffee_logs():
    """Get all coffee logs with coffee type names"""
    coffee_logs = CoffeeLog.query.all()
    result = []
    for cl in coffee_logs:
        # Get coffee type name for display
        coffee_type = CoffeeType.query.get(cl.coffee_type_id)
        coffee_type_name = coffee_type.name if coffee_type else f"Unknown Type {cl.coffee_type_id}"
        
        result.append({
            'id': cl.id,
            'user_id': cl.user_id,
            'coffee_type_id': cl.coffee_type_id,
            'coffee_type_name': coffee_type_name,
            'timestamp': cl.timestamp.isoformat(),
            'notes': cl.notes
        })
    return jsonify(result)


@app.route('/api/coffee-logs', methods=['POST'])
def create_coffee_log():
    """Create a new coffee log"""
    data = request.get_json()
    coffee_log = CoffeeLog(
        user_id=data['user_id'],
        coffee_type_id=data['coffee_type_id'],
        notes=data.get('notes', '')
    )
    db.session.add(coffee_log)
    db.session.commit()
    return jsonify({
        'id': coffee_log.id,
        'user_id': coffee_log.user_id,
        'coffee_type_id': coffee_log.coffee_type_id,
        'timestamp': coffee_log.timestamp.isoformat(),
        'notes': coffee_log.notes
    })