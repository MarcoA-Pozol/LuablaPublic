# Luabla - Language Learning with Decks

## 📌 Project Overview

Luabla is a language-learning web application built with Django. It follows the "deck of cards" methodology, allowing users to create, manage, and share their own decks of flashcards. Unlike other flashcard apps, Luabla provides an easy way to share decks through its built-in library, making language learning collaborative and accessible.

## ✨ Features

- Create and manage personalized flashcard decks
- Share decks publicly in the app's library
- Search and browse decks created by other users
- User authentication with JWT
- API endpoints for deck creation and retrieval (Django REST Framework)
- Rate limiting, pagination, and filtering for optimal API performance
- Redis caching for improved speed
- OpenAPI documentation for API exploration

## 🛠 Tech Stack

- **Backend:** Django, Django REST Framework (DRF)
- **Database:** PostgreSQL / MySQL
- **Authentication:** JWT
- **Caching:** Redis
- **Containerization:** Docker
- **API Documentation:** Swagger / OpenAPI
- **Frontend (if applicable):** React (optional, if integrated)

## 🚀 Installation & Setup

### Prerequisites

Ensure you have the following installed:

- Python (>= 3.9)
- PostgreSQL / MySQL
- Redis
- Docker (optional)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/luabla.git
   cd luabla
   ```
2. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Set up environment variables**
   - Create a `.env` file and configure database credentials, Redis URL, and JWT settings.
4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```
5. **Run the development server**
   ```bash
   python manage.py runserver
   ```
6. **(Optional) Run with Docker**
   ```bash
   docker-compose up --build
   ```

## 📖 Usage

- **Create a deck:** Users can create a deck of flashcards with words and translations.
- **Share a deck:** Users can add their decks to the public library for others to use.
- **Browse decks:** Search and find decks shared by other learners.
- **API Usage:** You can interact with the API using tools like Postman.

## 📜 API Documentation

- The API is documented using OpenAPI and accessible at:
  ```plaintext
  http://localhost:8000/api/docs/
  ```
  (Swagger UI enabled in development mode)

## 🛡 Security & Credentials

- Do **not** commit sensitive information like database passwords or JWT secrets.
- Use `.env` files for environment-specific configurations.
- Consider setting up `.gitignore` to exclude `.env` and other sensitive files.

## 🎯 Future Improvements

- Frontend integration (React-based UI)
- AI-based smart deck recommendations
- Mobile-friendly PWA version

## 🤝 Contributing

Contributions are welcome! Open an issue or submit a pull request if you have improvements.

## 📄 License

This project is licensed under the MIT License.

