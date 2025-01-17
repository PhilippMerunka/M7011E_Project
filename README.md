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

# API Documentation


## General Information
- **Base URL:** `/api/`
- **Authentication:** JSON Web Token (JWT)
  - Add the following header to authenticated requests:
    ```
    Authorization: Bearer <your_token>
    ```
- **Content-Type:** All requests should use `application/json` for the body.

---

## Endpoints

### Users

#### **POST /api/users/token/**
- **Purpose:** Returns a JWT for your credentials.
- **Arguments:**
  - `username` (string, required)
  - `password` (string, required)
- **Headers:** None.
- **Permissions:** Public (No authentication required).

#### **POST /api/users/register/**
- **Purpose:** Register a new user.
- **Arguments:**
  - `username` (string, required)
  - `password` (string, required)
  - `email` (string, required)
- **Headers:** None.
- **Permissions:** Public (No authentication required).

#### **POST /api/users/login/**
- **Purpose:** Authenticate a user and retrieve a JWT.
- **Arguments:**
  - `username` (string, required)
  - `password` (string, required)
- **Headers:** None.
- **Permissions:** Public (No authentication required).

#### **GET /api/users/profiles/**
- **Purpose:** Retrieve the authenticated user's profile(s).
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users can only view their profiles.

#### **POST /api/users/setup-2fa/**
- **Purpose:** Set up two-factor authentication.
- **Arguments:**
  - `code` (string, required)
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users only.

#### **DELETE /api/users/disable-2fa/**
- **Purpose:** Disable two-factor authentication.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users only.

---

### Products

#### **GET /api/products/products/**
- **Purpose:** List all products.
- **Headers:** None.
- **Permissions:** Public (No authentication required).
- **Filtering Options:**
  - `categories` (filter by category ID)
  - `price` (range filtering)
- **Search Options:**
  - `name`
  - `description`
- **Sorting Options:**
  - `price`
  - `name`

#### **POST /api/products/products/**
- **Purpose:** Create a new product.
- **Arguments:**
  - `name` (string, required)
  - `price` (float, required)
  - `description` (string, optional)
  - `categories` (list of IDs, optional)
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Admin only.

#### **GET /api/products/products/{id}/**
- **Purpose:** Retrieve details of a specific product.
- **Headers:** None.
- **Permissions:** Public.

#### **PATCH /api/products/products/{id}/**
- **Purpose:** Update details of a specific product.
- **Arguments:**
  - Partial updates are allowed.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Admin only.

#### **DELETE /api/products/products/{id}/**
- **Purpose:** Delete a product.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Admin only.

#### **GET /api/products/categories/**
- **Purpose:** List all categories.
- **Headers:** None.
- **Permissions:** Public.
- **Search Options:**
  - `name`
- **Sorting Options:**
  - `name`

#### **POST /api/products/categories/**
- **Purpose:** Create a new category.
- **Arguments:**
  - `name` (string, required)
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Admin only.

#### **GET /api/products/categories/{id}/**
- **Purpose:** Retrieve details of a specific category.
- **Headers:** None.
- **Permissions:** Public.

#### **PATCH /api/products/categories/{id}/**
- **Purpose:** Update a category.
- **Arguments:**
  - Partial updates are allowed.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Admin only.

#### **DELETE /api/products/categories/{id}/**
- **Purpose:** Delete a category.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Admin only.

---

### Carts

#### **GET /api/carts/carts/**
- **Purpose:** Retrieve the authenticated user's cart(s).
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users only.
- **Filtering Options:**
  - `user` (filter by user ID)
- **Search Options:**
  - `user__username`
- **Sorting Options:**
  - `created_at`

#### **POST /api/carts/carts/**
- **Purpose:** Create a cart for the authenticated user.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users only.

#### **GET /api/carts/carts/{id}/**
- **Purpose:** Retrieve details of a specific cart.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users can only access their carts.

#### **PATCH /api/carts/carts/{id}/**
- **Purpose:** Update a cart.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users can only update their carts.

#### **DELETE /api/carts/carts/{id}/**
- **Purpose:** Delete a cart.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users can only delete their carts.

---

### Orders

#### **GET /api/orders/orders/**
- **Purpose:** Retrieve the authenticated user's orders.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users only.
- **Filtering Options:**
  - `user`
  - `total`
  - `created_at`
- **Search Options:**
  - `user__username`
  - `user__email`
- **Sorting Options:**
  - `user__username`
  - `total`
  - `created_at`

#### **POST /api/orders/orders/**
- **Purpose:** Create an order from the authenticated user's cart.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users only.

#### **GET /api/orders/orders/{id}/**
- **Purpose:** Retrieve details of a specific order.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users can only access their orders.

#### **PATCH /api/orders/orders/{id}/**
- **Purpose:** Update an order.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users can only update their orders.

#### **DELETE /api/orders/orders/{id}/**
- **Purpose:** Delete an order.
- **Headers:**
  - `Authorization: Bearer <your_token>`
- **Permissions:** Authenticated users can only delete their orders.



## License
This project is licensed under the MIT License - see the LICENSE file for details.

