"""
Tests for database models
"""

import pytest
from app import app, db
from app.models import User, CoffeeType, CoffeeLog


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_create_user(client):
    """Test creating a user"""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'


def test_create_coffee_type(client):
    """Test creating a coffee type"""
    with app.app_context():
        # First create a user
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        # Then create a coffee type
        coffee_type = CoffeeType(
            name='Espresso',
            description='Strong black coffee',
            user_id=user.id
        )
        db.session.add(coffee_type)
        db.session.commit()
        
        assert coffee_type.id is not None
        assert coffee_type.name == 'Espresso'
        assert coffee_type.description == 'Strong black coffee'
        assert coffee_type.user_id == user.id


def test_create_coffee_log(client):
    """Test creating a coffee log"""
    with app.app_context():
        # Create user and coffee type first
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        coffee_type = CoffeeType(
            name='Espresso',
            description='Strong black coffee',
            user_id=user.id
        )
        db.session.add(coffee_type)
        db.session.commit()
        
        # Create coffee log
        coffee_log = CoffeeLog(
            user_id=user.id,
            coffee_type_id=coffee_type.id,
            notes='Morning coffee'
        )
        db.session.add(coffee_log)
        db.session.commit()
        
        assert coffee_log.id is not None
        assert coffee_log.user_id == user.id
        assert coffee_log.coffee_type_id == coffee_type.id
        assert coffee_log.notes == 'Morning coffee'