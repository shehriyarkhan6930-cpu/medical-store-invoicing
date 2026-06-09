import os
import sys
from app import create_app, db
from app.database import DatabaseManager

if __name__ == '__main__':
    # Create Flask app
    app = create_app()
    
    # Initialize database
    with app.app_context():
        DatabaseManager.initialize_database()
    
    # Run development server
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=True
    )
