from flask import request, jsonify, current_app
from flask_security import auth_required, login_user, logout_user, current_user
from application.models import User
from application.database import db
from werkzeug.security import check_password_hash, generate_password_hash
import uuid

def register_routes(app):
    @app.route('/', methods=['GET'])
    def health_check():
        """Health check endpoint for Railway"""
        return jsonify({
            'status': 'healthy',
            'message': 'LogiTrack API is running',
            'version': '1.0.0'
        })

    @app.route('/api/health', methods=['GET'])
    def api_health():
        """API health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'LogiTrack API is running',
            'version': '1.0.0'
        })

    @app.route('/api/login', methods=['POST', 'OPTIONS'])
    def login():
        if request.method == 'OPTIONS':
            return jsonify({'status': 'ok'}), 200
            
        try:
            data = request.get_json()
            if not data:
                return jsonify({'message': 'No data provided'}), 400
                
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'message': 'Username and password are required'}), 400
            
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password, password):
                login_user(user)
                # Generate auth token using Flask-Security method
                auth_token = user.get_auth_token()
                
                # Get user roles
                roles = [role.name for role in user.roles]
                
                return jsonify({
                    'message': 'Login successful',
                    'auth_token': auth_token,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': 'admin' if 'admin' in roles else 'user',
                        'created_at': user.fs_uniquifier  # Using fs_uniquifier as created_at placeholder
                    }
                }), 200
            else:
                return jsonify({'message': 'Invalid credentials'}), 401
                
        except Exception as e:
            current_app.logger.error(f"Login error: {str(e)}")
            return jsonify({'message': 'Login failed due to server error'}), 500

    @app.route('/api/register', methods=['POST', 'OPTIONS'])
    def register():
        if request.method == 'OPTIONS':
            return jsonify({'status': 'ok'}), 200
            
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
                
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            if not username or not email or not password:
                return jsonify({'error': 'Username, email, and password are required'}), 400
            
            if User.query.filter_by(username=username).first():
                return jsonify({'error': 'Username already exists'}), 400
            
            if User.query.filter_by(email=email).first():
                return jsonify({'error': 'Email already exists'}), 400
            
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                fs_uniquifier=str(uuid.uuid4())
            )
            
            # Add user role
            from application.models import Role
            user_role = Role.query.filter_by(name='user').first()
            if user_role:
                user.roles.append(user_role)
            
            db.session.add(user)
            db.session.commit()
            
            return jsonify({'message': 'User registered successfully'}), 201
            
        except Exception as e:
            current_app.logger.error(f"Registration error: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Registration failed due to server error'}), 500

    @app.route('/api/home', methods=['GET'])
    @auth_required('token')
    def home():
        roles = [role.name for role in current_user.roles]
        return jsonify({
            'user_id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'roles': roles
        })

    @app.route('/api/logout', methods=['POST'])
    @auth_required('token')
    def logout():
        logout_user()
        return jsonify({'message': 'Logged out successfully'})