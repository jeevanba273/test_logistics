# LogiTrack - Logistics Management System

A comprehensive logistics management system built with Flask (backend) and Vue.js (frontend).

## Features

### User Features
- **Authentication**: Secure login/registration system
- **Transaction Management**: Create, view, and manage shipment transactions
- **Payment Processing**: Pay for shipments with status tracking
- **Dashboard**: Overview of transactions and statistics
- **Profile Management**: View account information and activity

### Admin Features
- **Admin Dashboard**: System overview with comprehensive statistics
- **Transaction Management**: Update amounts, delivery dates, and statuses
- **User Management**: View all users and their transactions
- **System Analytics**: Revenue tracking and performance metrics

### Technical Features
- **Role-Based Access Control (RBAC)**: Admin and user roles with different permissions
- **RESTful API**: Clean API design with proper HTTP methods
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Real-time Updates**: Dynamic status updates and notifications
- **Modern UI/UX**: Clean, professional interface with animations

## Project Structure

```
├── backend/                 # Flask backend
│   ├── application/        # Application modules
│   │   ├── __init__.py
│   │   ├── config.py       # Configuration settings
│   │   ├── database.py     # Database setup
│   │   ├── models.py       # Database models
│   │   ├── resources.py    # API resources
│   │   └── routes.py       # Route handlers
│   ├── app.py             # Main application file
│   └── requirements.txt   # Python dependencies
│
└── frontend/              # Vue.js frontend
    ├── src/
    │   ├── components/    # Reusable components
    │   ├── stores/        # Pinia state management
    │   ├── services/      # API services
    │   ├── views/         # Page components
    │   └── router/        # Vue Router configuration
    ├── package.json       # Node.js dependencies
    └── tailwind.config.js # Tailwind CSS configuration
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## Default Credentials

- **Admin**: username: `admin01`, password: `1234`
- **User**: username: `user01`, password: `1234`

## API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration

### Transactions
- `GET /api/get` - Get all transactions
- `POST /api/create` - Create new transaction
- `PUT /api/update/<id>` - Update transaction
- `DELETE /api/delete/<id>` - Delete transaction

### Admin Operations
- `POST /api/update_amount/<id>` - Update transaction amount
- `PUT /api/update_delivery_status/<id>` - Update delivery status
- `POST /api/update_delivery_date/<id>` - Update delivery date

### User Operations
- `GET /api/pay/<id>` - Process payment
- `GET /api/review_transaction/<id>` - Get transaction details

## Technologies Used

### Backend
- **Flask** - Web framework
- **Flask-Security** - Authentication and authorization
- **Flask-SQLAlchemy** - ORM
- **Flask-RESTful** - REST API framework
- **SQLite** - Database

### Frontend
- **Vue.js 3** - Frontend framework
- **TypeScript** - Type safety
- **Pinia** - State management
- **Vue Router** - Routing
- **Tailwind CSS** - Styling
- **Heroicons** - Icons
- **Axios** - HTTP client
- **Vue Toastification** - Notifications

## License

This project is licensed under the MIT License.