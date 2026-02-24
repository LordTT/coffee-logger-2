"""
Tests for views/controllers
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


def test_index_page(client):
    """Test the index page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Coffee Logger' in response.data


def test_dashboard_page(client):
    """Test the dashboard page loads correctly"""
    # First create a user
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        # Simulate login by setting session
        with client.session_transaction() as sess:
            sess['user_id'] = user.id
            sess['username'] = user.username
    
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Coffee Dashboard' in response.data


def test_logs_page(client):
    """Test the logs page loads correctly"""
    # First create a user
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        # Simulate login by setting session
        with client.session_transaction() as sess:
            sess['user_id'] = user.id
            sess['username'] = user.username
    
    response = client.get('/logs')
    assert response.status_code == 200
    assert b'Coffee Logs' in response.data


def test_coffee_types_page(client):
    """Test the coffee types page loads correctly"""
    # First create a user
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        # Simulate login by setting session
        with client.session_transaction() as sess:
            sess['user_id'] = user.id
            sess['username'] = user.username
    
    response = client.get('/coffee-types')
    assert response.status_code == 200
    assert b'Coffee Types' in response.data


def test_api_users_endpoint(client):
    """Test the users API endpoint"""
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        # Test GET users
        response = client.get('/api/users')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['username'] == 'testuser'
        assert data[0]['email'] == 'test@example.com'


def test_api_coffee_types_endpoint(client):
    """Test the coffee types API endpoint"""
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        # Create a test coffee type
        coffee_type = CoffeeType(
            name='Espresso',
            description='Strong black coffee',
            user_id=user.id
        )
        db.session.add(coffee_type)
        db.session.commit()
        
        # Test GET coffee types
        response = client.get('/api/coffee-types')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['name'] == 'Espresso'
        assert data[0]['description'] == 'Strong black coffee'


def test_api_coffee_logs_endpoint(client):
    """Test the coffee logs API endpoint"""
    with app.app_context():
        # Create a test user and coffee type
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
        
        # Create a test coffee log
        coffee_log = CoffeeLog(
            user_id=user.id,
            coffee_type_id=coffee_type.id,
            notes='Morning coffee'
        )
        db.session.add(coffee_log)
        db.session.commit()
        
        # Test GET coffee logs
        response = client.get('/api/coffee-logs')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['notes'] == 'Morning coffee'