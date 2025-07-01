from flask import Flask
from flask_cors import CORS
from application.database import db
from application.models import User, Role
from application.config import LocalDevelopmentConfig, ProductionConfig
from flask_security import Security, datastore, SQLAlchemyUserDatastore, hash_password
from application.resources import api
from werkzeug.security import generate_password_hash, check_password_hash
import os

def create_app():
    app = Flask(__name__)
    
    # Use production config if FLASK_ENV is production
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
        # Get CORS origins from environment variable
        cors_origins = os.environ.get('CORS_ORIGINS', '').split(',')
        cors_origins = [origin.strip() for origin in cors_origins if origin.strip()]
        if not cors_origins:
            cors_origins = ["*"]  # Allow all origins if none specified (not recommended for production)
    else:
        app.config.from_object(LocalDevelopmentConfig)
        cors_origins = ["http://localhost:5173"]
    
    # Enable CORS
    CORS(app, origins=cors_origins, supports_credentials=True)
    
    db.init_app(app)
    api.init_app(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)
    app.app_context().push()
    return app

app = create_app()

with app.app_context():
    db.create_all()
    app.security.datastore.find_or_create_role(name='admin', description='Super user of app')
    app.security.datastore.find_or_create_role(name='user', description='Normal user of app')
    db.session.commit()

    if not app.security.datastore.find_user(email='user0@admin.com'):
        user = app.security.datastore.create_user(
            email='user0@admin.com',
            username='admin01',
            password=generate_password_hash('1234'),
            roles=['admin', 'user']
        )
    if not app.security.datastore.find_user(email='user01@user.com'):
        user = app.security.datastore.create_user(
            email='user01@user.com',
            username='user01',
            password=generate_password_hash('1234'),
            roles=['user']
        )
    db.session.commit()

from application.routes import *

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production')