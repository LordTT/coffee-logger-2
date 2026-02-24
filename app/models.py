"""
Database Models for Coffee Logger Application
"""

from app import db
from datetime import datetime


class User(db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    coffee_logs = db.relationship('CoffeeLog', backref='user', lazy=True)
    coffee_types = db.relationship('CoffeeType', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'


class CoffeeType(db.Model):
    """Coffee Type model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    coffee_logs = db.relationship('CoffeeLog', backref='coffee_type', lazy=True)
    
    def __repr__(self):
        return f'<CoffeeType {self.name}>'


class CoffeeLog(db.Model):
    """Coffee Log model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coffee_type_id = db.Column(db.Integer, db.ForeignKey('coffee_type.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<CoffeeLog {self.id}>'
