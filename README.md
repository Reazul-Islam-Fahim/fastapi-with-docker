# 🛒 E-Commerce Backend

A scalable, modular eCommerce backend built with **FastAPI**, **Docker**, and **Docker Compose**. This project provides RESTful APIs for managing products, users, orders, and authentication, ready for deployment and integration with any frontend.

---

## 🚀 Features

- 🔧 **FastAPI** for high-performance API development
- 🐳 **Dockerized** environment for consistent deployment
- 📦 **Docker Compose** for service orchestration
- 🔐 JWT-based Authentication
- 🗃️ SQL (PostgreSQL/MySQL) or NoSQL (MongoDB) support *(optional depending on your setup)*
- 🧪 Built-in testing setup (pytest)
- 📄 API documentation at `/docs` and `/redoc` (Swagger and ReDoc)

---

## 📁 Project Structure

.
*├── alembic
*│   ├── README
*│   ├── env.py
*│   ├── script.py.mako
*│   └── versions/
*├── alembic.ini
*├── auth
*│   ├── __init__.py
*│   ├── forgot_pass.py
*│   ├── login.py
*│   ├── registration.py
*│   └── security.py
*├── config.py
*├── crud
*│   ├── __init__.py
*│   ├── bank_details/
*│   ├── best_seller/
*│   ├── brands/
*│   ├── cart/
*│   ├── categories/
*│   ├── payments/
*│   └── product_features/
*├── database
*│   └── __init__.py
*├── docker-compose.yml
*├── Dockerfile
*├── main.py
*├── models
*│   └── __init__.py
*├── README.md
*├── requirements.txt
*├── resources/
*├── routes
*│   ├── __init__.py
*│   ├── bank_details/
*│   ├── best_seller/
*│   ├── brands/
*│   ├── categories/
*│   ├── sub_categories/
*│   └── users/
*├── schemas
*│   └── __init__.py
*├── utils/
*│   └── __init__.py
*├── .dockerignore
*└── .gitignore



