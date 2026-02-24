#!/usr/bin/env python3
"""
Initialize the database with sample data
"""

import os
import sys
from app import app, db
from app.models import User, CoffeeType, CoffeeLog

def init_db():
    """Initialize database with sample data"""
    
    # Create app context
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if data already exists
        if User.query.first() is not None:
            print("Database already initialized with data")
            return
            
        # Create sample users
        user1 = User(username='john_doe', email='john@example.com')
        user2 = User(username='jane_smith', email='jane@example.com')
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        print(f"Created users: {user1.username}, {user2.username}")
        
        # Create sample coffee types
        coffee_types_data = [
            ('Espresso', 'Strong black coffee'),
            ('Americano', 'Espresso with hot water'),
            ('Latte', 'Espresso with steamed milk'),
            ('Cappuccino', 'Espresso with steamed milk and foam'),
            ('Mocha', 'Espresso with chocolate and steamed milk')
        ]
        
        coffee_types = []
        for name, description in coffee_types_data:
            coffee_type = CoffeeType(
                name=name,
                description=description,
                user_id=user1.id
            )
            db.session.add(coffee_type)
            coffee_types.append(coffee_type)
            
        db.session.commit()
        print(f"Created coffee types: {[ct.name for ct in coffee_types]}")
        
        # Create sample coffee logs
        logs_data = [
            (user1.id, coffee_types[0].id, 'Morning coffee'),
            (user1.id, coffee_types[1].id, 'Afternoon espresso'),
            (user2.id, coffee_types[2].id, 'Breakfast latte'),
            (user1.id, coffee_types[3].id, 'Evening cappuccino'),
        ]
        
        for user_id, coffee_type_id, notes in logs_data:
            coffee_log = CoffeeLog(
                user_id=user_id,
                coffee_type_id=coffee_type_id,
                notes=notes
            )
            db.session.add(coffee_log)
            
        db.session.commit()
        print(f"Created {len(logs_data)} coffee logs")
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()