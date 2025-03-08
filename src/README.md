
#  DRF-Based E-Commerce API

A RESTful API for an e-commerce platform that allows users to browse and purchase products, while admins manage the system efficiently.


## Tech Stack
    1) Django – Python web framework for building the backend.
    2) Django REST Framework (DRF) – For creating RESTful APIs.
    3) Django Filters (django_filters) – For filtering querysets in APIs.
    4) JWT Authentication (rest_framework_simplejwt) – For secure authentication using JSON Web Tokens.
    5) Token Authentication (rest_framework.authtoken) – Alternative token-based authentication.
## Database
   PostgreSQL – The database management system used.
## primary programming language used

  python
##  Features
### User Features
- **Authentication & Profile Management**  
  - Register, login, logout (JWT-based authentication).  
  - View/update profile details (phone number, address).  
- **Product Browsing**  
  - View all products, filter by category, search by name/description.  
  - View product details and reviews.  
- **Shopping Cart**  
  - Add/update/remove items in the cart.  
  - View cart contents and total price.  
- **Order Management**  
  - Place orders, view order history, and track status (Pending, Shipped, Delivered).  
- **Reviews & Ratings**  
  - Submit ratings/comments for purchased products.  
  - View product reviews. 

### Admin Features
- **User Management**  
  - View all users, block/unblock users, delete accounts.  
- **Product Management**  
  - Create/update/delete products and categories (soft delete supported).  
- **Order Management**  
  - View all orders, update order status, or cancel orders.  

---

## Technologies Used
- **Backend**: Django & Django REST Framework  
- **Authentication**: JWT (JSON Web Tokens)  
- **Database**: PostgreSQL (configured via environment variables)  
- **Tools**: Postman (API testing)  

---


## Getting Started

### Prerequisites
- Python 3.9+  
- Pipenv (for dependency management)  

### Installation
1. Clone the repository:  
   ```bash
   git clone https://github.com/Anzilanzari/ecommerce-api.git
   cd ecommerce-api
## API Documentation (Postman) 
 ### Base URL
 - http://127.0.0.1:8000/api/v1/

 ### Authentication
 - Register: POST- /authentication/register/
 - Login: POST /authentication/login/ (Returns JWT tokens)
 - Logout: POST /authentication/logout/ (Requires refresh token)
 - Include JWT in headers for authenticated endpoints:
    Authorization: Bearer {{usertoken}}

## API Endpoints

### Authentication & Profile
| Method | Endpoint                          | Description                          |
|--------|-----------------------------------|--------------------------------------|
| POST   | `/authentication/register/`       | User registration                    |
| POST   | `/authentication/login/`          | User login (returns JWT tokens)      |
| POST   | `/authentication/logout/`         | Logout (requires refresh token)      |
| GET    | `/authentication/profile/`        | View user profile                    |
| PUT    | `/authentication/update-profile/` | Update profile (e.g., phone number)  |

### Products
| Method | Endpoint                                  | Description                          |
|--------|-------------------------------------------|--------------------------------------|
| GET    | `/product_manage/products/`               | List all products                    |
| GET    | `/product_manage/products/?search=query`  | Search products by name/description  |
| GET    | `/product_manage/products/5/`             | View details of product ID 5         |
| GET    | `/product_manage/categories/cbv/`         | List all categories                  |
| GET    | `/product_manage/categories/cbv/1/`       | Filter products by category ID 1     |

### Cart
| Method | Endpoint                      | Description                      |
|--------|-------------------------------|----------------------------------|
| POST   | `/product_manage/cart/`       | Add item to cart                 |
| PUT    | `/product_manage/cart/4/`     | Update quantity of cart item ID 4|
| DELETE | `/product_manage/cart/4/`     | Remove cart item ID 4            |
| GET    | `/product_manage/cart/`       | View cart contents               |

### Orders
| Method | Endpoint                              | Description                      |
|--------|---------------------------------------|----------------------------------|
| POST   | `/product_manage/orders/place/`       | Place order from cart            |
| GET    | `/product_manage/orders/history/`     | View order history               |
| GET    | `/product_manage/orders/3/`           | View details of order ID 3       |

### Reviews & Ratings
| Method | Endpoint                                  | Description                      |
|--------|-------------------------------------------|----------------------------------|
| POST   | `/product_manage/products/3/reviews/`     | Submit review for product ID 3   |
| GET    | `/product_manage/products/3/reviews/list/`| View reviews for product ID 3    |

### Admin Endpoints
| Method | Endpoint                                  | Description                      |
|--------|-------------------------------------------|----------------------------------|
| GET    | `/admin_manage/users/`                    | List all users                   |
| POST   | `/admin_manage/users/2/block/`            | Block user ID 2                  |
| POST   | `/admin_manage/users/2/unblock/`          | Unblock user ID 2                |
| DELETE | `/admin_manage/users/delete/2/`           | Delete user ID 2                 |
| GET    | `/product_manage/admin/orders/`           | List all orders (admin view)     |
| PUT    | `/product_manage/admin/orders/3/`         | Update status of order ID 3      |
| DELETE | `/product_manage/admin/orders/4/`         | Delete order ID 4                |
| POST   | `/product_manage/categories/`             | Create a new category            |
| PUT    | `/product_manage/categories/cbv/1/`       | Update category ID 1             |
| DELETE | `/product_manage/categories/cbv/3/`       | Delete category ID 3             |

## Postman Setup
#### 1. Import the provided ecommerce.postman_collection.json.
#### 2. Set environment variables
     - usertoken: JWT access token obtained after user login.
     - admintoken: Admin JWT token (login as admin first).
## Setting Up the Virtual Environment
- Windows Command Prompt : ..\..\venv\scripts\activate
## Start the server:
- python manage.py runserver## User Registration Example

### Request
- **Method**: `POST`
- **Endpoint**: `/api/v1/authentication/register/`
- **Content-Type**: `multipart/form-data`

#### Form Data
| Key           | Value               |
|---------------|---------------------|
| `username`    | `userone`           |
| `password`    | `userone`           |
| `email`       | `userone@gmail.com` |
| `phone_number`| `1234567890`        |
| `address`     | `Kerala,India`      |

#### Example Request (cURL)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/authentication/register/


{
  "id": 1,
  "username": "userone",
  "email": "userone@gmail.com",
  "phone_number": "1234567890",
  "address": "Kerala,India",
  "message": "User registered successfully"
}
