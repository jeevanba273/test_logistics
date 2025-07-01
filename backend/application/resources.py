from flask_restful import Api, Resource, reqparse
from flask_security import auth_required, current_user
from application.models import Transaction, User
from application.database import db
from flask import jsonify

api = Api()

class TransactionListAPI(Resource):
    @auth_required()
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

    @auth_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=False, default='Shipment')
            parser.add_argument('type', required=False, default='delivery')
            parser.add_argument('date', required=False)
            parser.add_argument('delivery_date', required=True)
            parser.add_argument('source_city', required=False, default='Origin')
            parser.add_argument('destination_city', required=False, default='Destination')
            parser.add_argument('description', required=False, default='')
            parser.add_argument('amount', type=float, required=True)
            parser.add_argument('status', required=False, default='pending')
            args = parser.parse_args()

            # Use current date if not provided
            import datetime
            transaction_date = args.get('date') or datetime.datetime.now().strftime('%Y-%m-%d')

            transaction = Transaction(
                name=args['name'],
                user_id=current_user.id,
                type=args['type'],
                date=transaction_date,
                delivery_date=args['delivery_date'],
                source_city=args['source_city'],
                destination_city=args['destination_city'],
                description=args.get('description', ''),
                amount=args['amount'],
                delivery_status=args.get('status', 'pending'),
                internal_status='requested'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            return {'message': 'Transaction created successfully', 'id': transaction.id}, 201
        except Exception as e:
            return {'error': str(e)}, 500

api.add_resource(TransactionListAPI, '/api/get', '/api/create')

class TransactionAPI(Resource):
    @auth_required()
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

    @auth_required()
    def put(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            parser = reqparse.RequestParser()
            parser.add_argument('name')
            parser.add_argument('type')
            parser.add_argument('date')
            parser.add_argument('delivery_date')
            parser.add_argument('source_city')
            parser.add_argument('destination_city')
            parser.add_argument('description')
            parser.add_argument('amount', type=float)
            parser.add_argument('status')
            args = parser.parse_args()

            for key, value in args.items():
                if value is not None:
                    if key == 'status':
                        setattr(transaction, 'delivery_status', value)
                    else:
                        setattr(transaction, key, value)
            
            db.session.commit()
            return {'message': 'Transaction updated successfully'}
        except Exception as e:
            return {'error': str(e)}, 500

    @auth_required()
    def delete(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            db.session.delete(transaction)
            db.session.commit()
            return {'message': 'Transaction deleted successfully'}
        except Exception as e:
            return {'error': str(e)}, 500

api.add_resource(TransactionAPI, '/api/update/<int:transaction_id>', '/api/delete/<int:transaction_id>', '/api/review_transaction/<int:transaction_id>')

class PaymentAPI(Resource):
    @auth_required()
    def get(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            transaction.internal_status = 'paid'
            db.session.commit()
            return {'message': 'Payment processed successfully'}
        except Exception as e:
            return {'error': str(e)}, 500

api.add_resource(PaymentAPI, '/api/pay/<int:transaction_id>')

class UpdateAmountAPI(Resource):
    @auth_required()
    def post(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            parser = reqparse.RequestParser()
            parser.add_argument('amount', type=float, required=True)
            args = parser.parse_args()
            
            transaction.amount = args['amount']
            transaction.internal_status = 'Payment Pending'
            db.session.commit()
            return {'message': 'Amount updated successfully'}
        except Exception as e:
            return {'error': str(e)}, 500

api.add_resource(UpdateAmountAPI, '/api/update_amount/<int:transaction_id>')

class UpdateDeliveryStatusAPI(Resource):
    @auth_required()
    def put(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            parser = reqparse.RequestParser()
            parser.add_argument('delivery_status', required=True)
            args = parser.parse_args()
            
            transaction.delivery_status = args['delivery_status']
            db.session.commit()
            return {'message': 'Delivery status updated successfully'}
        except Exception as e:
            return {'error': str(e)}, 500

api.add_resource(UpdateDeliveryStatusAPI, '/api/update_delivery_status/<int:transaction_id>')

class UpdateDeliveryDateAPI(Resource):
    @auth_required()
    def put(self, transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            parser = reqparse.RequestParser()
            parser.add_argument('delivery_date', required=True)
            args = parser.parse_args()
            
            transaction.delivery_date = args['delivery_date']
            db.session.commit()
            return {'message': 'Delivery date updated successfully'}
        except Exception as e:
            return {'error': str(e)}, 500

api.add_resource(UpdateDeliveryDateAPI, '/api/update_delivery_date/<int:transaction_id>')