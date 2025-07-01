from flask_restful import Api, Resource, reqparse
from flask_security import auth_required, current_user
from application.models import Transaction, User
from application.database import db
from flask import jsonify, request
import datetime

api = Api()

class TransactionListAPI(Resource):
    @auth_required('token')
    def get(self):
        try:
            transactions = Transaction.query.all()
            result = []
            for transaction in transactions:
                user = User.query.get(transaction.user_id)
                result.append({
                    'id': transaction.id,
                    'name': transaction.name,
                    'user_id': transaction.user_id,
                    'user': {'username': user.username, 'email': user.email} if user else None,
                    'type': transaction.type,
                    'date': transaction.date,
                    'delivery_date': transaction.delivery_date,
                    'source_city': transaction.source_city,
                    'destination_city': transaction.destination_city,
                    'internal_status': transaction.internal_status,
                    'delivery_status': transaction.delivery_status,
                    'description': transaction.description,
                    'amount': transaction.amount,
                    'status': transaction.delivery_status,  # Map to frontend expected field
                    'payment_status': 'paid' if transaction.internal_status == 'paid' else 'pending',
                    'created_at': transaction.date,  # Using date as created_at
                    'updated_at': transaction.date   # Using date as updated_at
                })
            return result
        except Exception as e:
            return {'error': str(e)}, 500

    @auth_required('token')
    def post(self):
        try:
            # Get JSON data from request
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400

            # Extract required fields
            amount = data.get('amount')
            delivery_date = data.get('delivery_date')
            
            if not amount or not delivery_date:
                return {'error': 'Amount and delivery date are required'}, 400

            # Use current date if not provided
            transaction_date = data.get('date') or datetime.datetime.now().strftime('%Y-%m-%d')

            transaction = Transaction(
                name=data.get('name', 'Shipment'),
                user_id=current_user.id,
                type=data.get('type', 'delivery'),
                date=transaction_date,
                delivery_date=delivery_date,
                source_city=data.get('source_city', 'Origin'),
                destination_city=data.get('destination_city', 'Destination'),
                description=data.get('description', ''),
                amount=float(amount),
                delivery_status=data.get('status', 'pending'),
                internal_status='requested'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            return {'message': 'Transaction created successfully', 'id': transaction.id}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def options(self):
        return {'status': 'ok'}, 200

api.add_resource(TransactionListAPI, '/api/get', '/api/create')

class TransactionAPI(Resource):
    @auth_required('token')
    def get(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            user = User.query.get(transaction.user_id)
            return {
                'id': transaction.id,
                'name': transaction.name,
                'user_id': transaction.user_id,
                'user': {'username': user.username, 'email': user.email} if user else None,
                'type': transaction.type,
                'date': transaction.date,
                'delivery_date': transaction.delivery_date,
                'source_city': transaction.source_city,
                'destination_city': transaction.destination_city,
                'internal_status': transaction.internal_status,
                'delivery_status': transaction.delivery_status,
                'description': transaction.description,
                'amount': transaction.amount,
                'status': transaction.delivery_status,
                'payment_status': 'paid' if transaction.internal_status == 'paid' else 'pending',
                'created_at': transaction.date,
                'updated_at': transaction.date
            }
        except Exception as e:
            return {'error': str(e)}, 500

    @auth_required('token')
    def put(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400

            # Update fields if provided
            for key, value in data.items():
                if value is not None:
                    if key == 'status':
                        setattr(transaction, 'delivery_status', value)
                    elif hasattr(transaction, key):
                        setattr(transaction, key, value)
            
            db.session.commit()
            return {'message': 'Transaction updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    @auth_required('token')
    def delete(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            db.session.delete(transaction)
            db.session.commit()
            return {'message': 'Transaction deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def options(self, transaction_id=None):
        return {'status': 'ok'}, 200

api.add_resource(TransactionAPI, '/api/update/<int:transaction_id>', '/api/delete/<int:transaction_id>', '/api/review_transaction/<int:transaction_id>')

class PaymentAPI(Resource):
    @auth_required('token')
    def get(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            transaction.internal_status = 'paid'
            db.session.commit()
            return {'message': 'Payment processed successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def options(self, transaction_id=None):
        return {'status': 'ok'}, 200

api.add_resource(PaymentAPI, '/api/pay/<int:transaction_id>')

class UpdateAmountAPI(Resource):
    @auth_required('token')
    def post(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            data = request.get_json()
            
            if not data or 'amount' not in data:
                return {'error': 'Amount is required'}, 400
            
            transaction.amount = float(data['amount'])
            transaction.internal_status = 'Payment Pending'
            db.session.commit()
            return {'message': 'Amount updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def options(self, transaction_id=None):
        return {'status': 'ok'}, 200

api.add_resource(UpdateAmountAPI, '/api/update_amount/<int:transaction_id>')

class UpdateDeliveryStatusAPI(Resource):
    @auth_required('token')
    def put(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            data = request.get_json()
            
            if not data or 'delivery_status' not in data:
                return {'error': 'Delivery status is required'}, 400
            
            transaction.delivery_status = data['delivery_status']
            db.session.commit()
            return {'message': 'Delivery status updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def options(self, transaction_id=None):
        return {'status': 'ok'}, 200

api.add_resource(UpdateDeliveryStatusAPI, '/api/update_delivery_status/<int:transaction_id>')

class UpdateDeliveryDateAPI(Resource):
    @auth_required('token')
    def put(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            data = request.get_json()
            
            if not data or 'delivery_date' not in data:
                return {'error': 'Delivery date is required'}, 400
            
            transaction.delivery_date = data['delivery_date']
            db.session.commit()
            return {'message': 'Delivery date updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def options(self, transaction_id=None):
        return {'status': 'ok'}, 200

api.add_resource(UpdateDeliveryDateAPI, '/api/update_delivery_date/<int:transaction_id>')