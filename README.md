# URL Shortener API

## 📑 Introduction

Welcome to the URL Shortener API, a robust and scalable solution designed to transform lengthy URLs into concise, shareable links. This project addresses the common challenge of sharing unwieldy URLs across platforms where character count matters, such as social media, messaging applications, and email communications.

Built with modern web development technologies, this API provides not only basic URL shortening capabilities but also advanced features like click analytics, user authentication, and custom URL slug creation. The combination of FastAPI's asynchronous performance with PostgreSQL's reliability creates a service that is both lightning-fast and dependable.

## 📋 Table of Contents

- [Introduction](#-introduction)
- [Live Demo](#-live-demo)
- [Application Architecture](#️-application-architecture)
- [Features](#-features)
- [API Endpoints Overview](#-api-endpoints-overview)
- [Technologies Used](#-technologies-used)
- [Live Deployment Setup](#-live-deployment-setup)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🚀 Live Demo

The API is currently live at: [https://url-shortener-api-qjgk.onrender.com/docs](https://url-shortener-api-qjgk.onrender.com/docs)

Or try at: [https://url-shortener-api-qjgk.onrender.com/redoc](https://url-shortener-api-qjgk.onrender.com/redoc)

## 👷‍♂️ Application Architecture

![Image](https://github.com/user-attachments/assets/e7841723-5edd-4bc7-9082-b1870496970a)

The URL Shortener API is built with FastAPI and uses PostgreSQL as its database for storing URL mappings and metadata. Database migrations are managed with Alembic, ensuring smooth schema updates across environments. The project includes a robust testing setup using Pytest and FastAPI’s TestClient to validate routes, database operations, and edge cases. It is fully containerized with Docker and orchestrated using Docker Compose, making it easy to deploy and scale across any environments. Reverse proxy handles ssl/tls handeshake and termination for secure communication with the help of Nginx which then forward the plain http to gunicorn a python http server.

## 🔧 Development Setup

To spin up this project run the following commands:

1. Clone the repository:

   ```bash
   git clone https://github.com/mohit-d13/url-shortener-api.git
   ```

2. Go inside project directory:

   ```bash
   cd URL_SHORTENER_API
   ```

3. Create a `.env` file in the project root:

   ```.env
   DB_USERNAME="your_username"
   DB_PASSWORD="your_password"
   DB_HOST="localhost"
   DB_PORT=5432
   DB_NAME="database_name" 
   SECRET_KEY="your_secret_key"    
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL="postgresql://your_username:your_password@db:5432/database_name"
   ```

4. To genrate a random secret key use this command and copy the output to the variable `SECRET_KEY` in your `.env` file:

   ```bash
   openssl rand -hex 32
   ```

5. Generate a self signed certificate and key for ssl connection, provide neccessary information to generate the certificate:

   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout private.key -out certificate.crt -days 365 -nodes -sha256
   ```

6. Copy the `.crt` and `.key` file into project dir `./proxy/ssl`

   ```bash
   cp .crt ./proxy/ssl
   cp .key ./proxy/ssl
   ```

7. Run docker compose command:

   ```bash
   docker compose up --build
   ```

If you done the all the steps write your project should be running at `https://localhost:444`
Note:- Your browser going show you not secure because the ssl certificate is self signed.

## ✨ Features

- Create shortened URLs from long URLs
- Custom slug option for personalized short links
- URL analytics tracking (clicks, referrers, etc.)
- User authentication and management
- REST API with comprehensive documentation
- Database migrations using Alembic
- Unit testing with pytest and Testclient
- Containerized with docker
- Nginx as reverse proxy for SSL Termination

## 📘 API Endpoints Overview

### 🔐 User / Authentication

- `POST /signup/`: Create your profile
- `POST /login/`: Authenticate yourself
- `GET  /user/me`: View your profile

### 🔗 URL Operations

- `POST /sites/`: Create a short URL
- `GET /sites/all`: Get all your created URLs
- `GET /sites/info/{url_key}/`: Get analysis details of an URL
- `GET /{url_key}`: Redirect to the original URL
- `DELETE /{url_key}`: Delete a URL

## 🧠 Technologies Used

- **FastAPI**: Web Api framework
- **PostgreSQL**: Database
- **Alembic**: Database migrations tool
- **Pytest**: Automated Tests
- **User-Agent Parser**: For Tracking user device/browser
- **Docker**: Containerized development and deployment
- **Render**: Live deployment website
- **Gunicorn**: Python http server
- **Nginx**: Used as a reverse Proxy

## 🚀 Live Deployment Setup

This project is deployed on Render. Follow these steps to deploy your own instance:

1. Create a PostgreSQL database on Render
2. Create a Web Service for the API
3. Set environment variables
4. Connect to your GitHub repository
5. Deploy!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📬 Contact

For questions or feedback, please open an issue or contact [your email or contact info].
