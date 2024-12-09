# Dynamic Web Systems Project

## Overview
This is the final project of the M7011E Design of Dynamic Web System course. 

## Features
- **Microservices Architecture**: Divides functionality into services like user management, product catalog, and order management.
- **Role-based Authorization**: Supports different user roles (e.g., Regular User, Admin, Super User).
- **CRUD Operations**: Create, Read, Update, Delete operations for all entities using Django REST Framework.
- **Authentication**: Supports both Basic Auth and OAuth using Google.
- **Two-Factor Authentication (2FA)**: Secure access using Google Authenticator.
- **Third-party packages**: Integrates welcome-emails using SendGrid and Django
- **Unit testing**: Complete unit tests for the user and products modules

## Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/PhilippMerunka/M7011E_Project.git
   cd M7011E_Project
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3.  **Setup PostgreSQL**
4. **Environment Variables**:
   - Create an `.env` in the root directory and add the following credentials:
      - GOOGLE_OAUTH_CLIENT_ID
      - GOOGLE_OAUTH_CLIENT_SECRET
      - EMAIL_HOST_USER: API username
      - EMAIL_HOST_PASSWORD: API key
      - EMAIL_FROM_USER: E-Mail to be sent from

5. **Run Database Migrations**:
   ```bash
   python manage.py makemigrations
   ```
   ```bash
   python manage.py migrate
   ```
6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
7. **Testing**
   - Ensure the user has sufficient privileges
   
   ```bash
   ALTER USER <username> CREATEDB;
   ```
   - Run the tests
   
   ```bash
   python manage.py test
   ```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

