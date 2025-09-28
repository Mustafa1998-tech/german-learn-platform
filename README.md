# German Learning Platform

A comprehensive web application for learning German, featuring lessons from A1 to C2 levels, interactive exercises, and audio support.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Features

- **Structured Learning Path**: Progress from A1 (beginner) to C2 (proficiency) levels
- **Interactive Lessons**: Engaging content with text, audio, and video
- **Vocabulary Builder**: Learn and practice new words with translations
- **Interactive Exercises**: Test your knowledge with various exercise types
- **Progress Tracking**: Monitor your learning journey
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Docker Support**: Easy containerization for development and production
- **Cloud Ready**: One-click deployment to Render

## Prerequisites

### For Local Development
- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)
- Docker and Docker Compose (for containerized development)

## Quick Start with Docker (Recommended)

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/german-learning-platform.git
   cd german-learning-platform
   ```

2. **Create .env file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and start containers**
   ```bash
   docker-compose up --build -d
   ```

4. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access the application**
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/
   - PostgreSQL: localhost:5432
   - PgAdmin (if enabled): http://localhost:5050

## Manual Installation (Without Docker)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/german-learning-platform.git
   cd german-learning-platform
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin) account**
   ```bash
   python manage.py createsuperuser
   ```

7. **Import initial data**
   ```bash
   python manage.py import_youtube_courses
   ```

8. **Generate audio files** (requires internet connection)
   ```bash
   python manage.py generate_audio
   ```

## Development

### Running the Development Server

With Docker:
```bash
docker-compose up --build
```

Without Docker:
```bash
python manage.py runserver
```

### Accessing the Application
- Main site: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/api/docs/

### Running Tests

```bash
# With Docker
docker-compose exec web python manage.py test

# Without Docker
python manage.py test
```

### Linting and Code Style

```bash
# Run flake8
flake8

# Run black
black .
```

## Project Structure

```
german_learning_platform/
├── .github/                   # GitHub workflows and issue templates
├── courses/                   # Main app
│   ├── management/commands/   # Custom management commands
│   ├── migrations/            # Database migrations
│   ├── static/                # Static files (CSS, JS, images)
│   ├── templates/             # HTML templates
│   ├── admin.py               # Admin configuration
│   ├── apps.py                # App configuration
│   ├── models.py              # Database models
│   ├── urls.py                # URL routing
│   └── views.py               # View functions
├── german_learning_platform/  # Project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py            # Base settings
│   │   ├── development.py     # Development settings
│   │   └── production.py      # Production settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py
├── media/                     # User-uploaded files
├── static/                    # Global static files
├── nginx/                     # Nginx configuration
│   └── nginx.conf
├── .dockerignore              # Files ignored by Docker
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore file
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Dockerfile for production
├── Dockerfile.dev             # Dockerfile for development
├── manage.py                  # Django management script
├── README.md                  # This file
├── requirements.txt           # Development dependencies
└── requirements_prod.txt      # Production dependencies
```

## Deployment

### Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Click the "Deploy to Render" button above
2. Connect your GitHub repository
3. Select the appropriate plan (Free tier available)
4. Click "Create Web Service"
5. Add your environment variables in the Render dashboard

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Django
DEBUG=0
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=.onrender.com,your-custom-domain.com

# Database
DB_NAME=german_learning
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=5432
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# Email (optional)
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@example.com
```

### Updating the Deployment

When you push changes to your repository, Render will automatically rebuild and redeploy your application.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Docker](https://www.docker.com/)
- [Render](https://render.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)

## Custom Management Commands

- `import_youtube_courses`: Imports initial data (levels, lessons, exercises)
  ```bash
  python manage.py import_youtube_courses
  ```

- `generate_audio`: Generates audio files for lessons using gTTS
  ```bash
  python manage.py generate_audio
  # Options:
  # --force: Regenerate all audio files
  # --lesson-id: Generate audio for a specific lesson
  ```

## Deployment

For production deployment, consider using:
- Web server: Nginx or Apache
- Application server: Gunicorn or uWSGI
- Database: PostgreSQL or MySQL
- Media storage: AWS S3 or similar

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework used
- [Bootstrap 5](https://getbootstrap.com/) - Frontend framework
- [gTTS](https://pypi.org/project/gTTS/) - Google Text-to-Speech
- [Font Awesome](https://fontawesome.com/) - Icons

---

**Note**: This project is for educational purposes. The content is auto-generated and may contain inaccuracies.
