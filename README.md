# URL Shortener API

## Introduction

Welcome to the URL Shortener API, a robust and scalable solution designed to transform lengthy URLs into concise, shareable links. This project addresses the common challenge of sharing unwieldy URLs across platforms where character count matters, such as social media, messaging applications, and email communications.

Built with modern web development technologies, this API provides not only basic URL shortening capabilities but also advanced features like click analytics, user authentication, and custom URL slug creation. The combination of FastAPI's asynchronous performance with PostgreSQL's reliability creates a service that is both lightning-fast and dependable.

Whether you're looking to integrate URL shortening into your own application, analyze click-through rates for marketing campaigns, or simply make your links more manageable, this API offers a comprehensive solution that balances simplicity with powerful functionality.

The project follows industry best practices including comprehensive API documentation, database migrations for version control, and secure authentication mechanisms. It's designed to be easily deployable and maintainable, making it suitable for both personal projects and production environments.

## 🚀 Live Demo

The API is currently live at: [https://url-shortener-api-qjgk.onrender.com/docs](https://url-shortener-api-qjgk.onrender.com/docs)

Or try at: [https://url-shortener-api-qjgk.onrender.com/redoc](https://url-shortener-api-qjgk.onrender.com/redoc)




## 📋 Table of Contents

- [Introduction](#-introduction)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Technologies Used](#technologies-used)
- [Websocket Configuration](#websocket-configuration)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [File Upload Process](#file-upload-process)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## ✨ Features

- Create shortened URLs from long URLs
- Custom slug option for personalized short links
- URL analytics tracking (clicks, referrers, etc.)
- User authentication and management
- REST API with comprehensive documentation
- Database migrations using Alembic

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

## 🗄️ Database Schema

- **Site Table**: Stores mapping between short and original URLs
- **Click Table**: Tracks click analytics for each short URL
- **User Table**: Manages user authentication and permissions

## 🧠 Technologies Used

- **FastAPI**: Web framework
- **PostgreSQL**: Database
- **SQLAlchemy**: ORM layer
- **Alembic**: Database migrations tool
- **PyJWT**: Token-based authentication
- **User-Agent Parser**: For Tracking user device/browser
- **Render**: Live deployment website


## 🔧 Local Development Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mohit-d13/url-shortener-api.git
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Mac: venv/bin/activate 
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   DB_USERNAME=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=database_name
   SECRET_KEY=your_secret_key
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the development server:
   ```bash
   fastapi dev app/main.py
   ```

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