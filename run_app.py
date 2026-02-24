#!/usr/bin/env python3
"""
Run the Coffee Logger application
"""

import os
from app import app, db

def main():
    """Main function to run the application"""
    # Initialize database
    with app.app_context():
        db.create_all()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()