# Dynamic Web Systems Project

## Overview
This is the final project of the M7011E Design of Dynamic Web System course. 

## Proposed Project Structure

```
Root Directory
├── README.md              # Overview and setup instructions
├── .env                   # Environment variables (e.g., database credentials)
├── docker-compose.yml     # Docker setup for containerizing services (optional)
├── requirements.txt       # List of Python dependencies
└── manage.py              # Django management script

Backend (Django)
├── /project_name/         # Main Django project folder
│   ├── __init__.py
│   ├── settings.py        # Configuration for the Django project
│   ├── urls.py            # Root URL configurations
│   └── wsgi.py            # Web server gateway interface
├── /apps/                 # Custom apps directory (microservices)
│   ├── /users/            # User management app
│   │   ├── models.py      # User models, including roles
│   │   ├── views.py       # Views for user CRUD operations
│   │   ├── serializers.py # Serializers for API responses
│   │   ├── urls.py        # Endpoints for user management
│   │   └── tests.py       # Unit tests for user operations
│   ├── /products/         # Product management app
│   │   └── (Similar structure as users app)
│   └── /orders/           # Order management app
│       └── (Similar structure as users app)
├── /api/                  # Central API layer to aggregate different microservice endpoints
│   └── urls.py            # API URL patterns for different microservices
└── /integrations/         # Folder to manage external services
    ├── /email/            # Email integration using Django Email
    ├── /s3_storage/       # AWS S3 storage integration
    └── /authentication/   # OAuth or JWT integration

Templates & Static Files
├── /templates/            # Basic templates for the web application (optional)
└── /static/               # Static files (CSS, JavaScript, images)

Tests
└── /tests/                # Centralized testing folder
    ├── Unit Tests         # Tests for individual components
    └── Integration Tests  # End-to-end tests to ensure the whole application works

Deployment
└── /deployment/           # Files related to deployment
    ├── Dockerfile         # Docker configuration for containerization
    └── heroku.yml or AWS setup scripts # Deployment scripts
```

## Proposed Technologies Used
- **Backend**: Django
- **Database**: PostgreSQL
- **Message Broker**: CloudAMQP (RabbitMQ)
- **Authentication**: Basic Auth, OAuth/JWT, 2FA (Twilio/Google Authenticator)
- **Deployment**: Heroku/AWS
- **Documentation**: Swagger/Postman
- **Testing**: Pytest

## Features TO-DO
### Backend
- **Microservices Architecture**: Divides functionality into services like user management, product catalog, and order management.
- **Role-based Authorization**: Supports different user roles (e.g., Regular User, Admin, Super User).
- **CRUD Operations**: Create, Read, Update, Delete operations for all entities using Django REST Framework.
- **Authentication**: Supports both Basic Auth and advanced OAuth/JWT methods.
- **Two-Factor Authentication (2FA)**: Secure access using services like Twilio or Google Authenticator.

### Third-party Integration
- **Email Notifications**: Integrated using Django's email utilities.
- **AWS S3 Storage**: Supports user file uploads to S3.

### Testing & Deployment
- **Unit and Integration Testing**: Ensures code quality and functionality.
- **Docker Support**: Option to run services in isolated containers.
- **Deployment**: Ready for deployment on platforms like Heroku or AWS.

## Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variables**:
   - Copy `.env.example` to `.env` and fill in the required credentials.

4. **Run Database Migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

