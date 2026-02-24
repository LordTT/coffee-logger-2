"""
Views/Controllers for Coffee Logger Application
"""

from app import app, db
from app.models import User, CoffeeType, CoffeeLog
from flask import render_template, request, redirect, url_for, jsonify
import json


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')


@app.route('/logs')
def logs():
    """Logs page"""
    return render_template('logs.html')


@app.route('/coffee-types')
def coffee_types():
    """Coffee types page"""
    return render_template('coffee_types.html')


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
    """Get all coffee logs"""
    coffee_logs = CoffeeLog.query.all()
    return jsonify([{
        'id': cl.id,
        'user_id': cl.user_id,
        'coffee_type_id': cl.coffee_type_id,
        'timestamp': cl.timestamp.isoformat(),
        'notes': cl.notes
    } for cl in coffee_logs])


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