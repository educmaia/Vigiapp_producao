#!/usr/bin/env python3
import os
from app import create_app, db

def init_database(app):
    """Initialize database and create default admin user"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default admin user if it doesn't exist
        from werkzeug.security import generate_password_hash
        from models import User
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@vigiapp.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print('Default admin user created')

if __name__ == '__main__':
    app = create_app()
    
    # Registrar o filtro nl2br
    import markupsafe
    def nl2br(value):
        if value:
            return markupsafe.Markup(
                markupsafe.escape(value).replace('\n', markupsafe.Markup('<br>\n'))
            )
        return ''
    
    app.jinja_env.filters['nl2br'] = nl2br
    
    # Initialize database
    init_database(app)
    
    # Run the application
    app.run(debug=False, host='0.0.0.0', port=5000)