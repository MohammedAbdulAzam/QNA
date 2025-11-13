# QNA - Quiz Management System

A full-stack web application for creating, managing, and taking quizzes with role-based access control.

## Features

### For Quiz Masters (Admins)
- Complete CRUD operations for subjects, chapters, quizzes, and questions
- User management and monitoring
- Quiz attempt tracking and statistics
- System-wide analytics with Chart.js visualizations
- Subject search functionality

### For Users
- Browse subjects and chapters
- Take timed multiple-choice quizzes
- Real-time countdown timer
- Automatic quiz submission on timeout
- View detailed quiz results with correct answers
- Performance tracking across subjects
- Profile management

## Tech Stack

**Backend:**
- Python 3.12
- Flask 3.1.0
- SQLAlchemy (ORM)
- Flask-Login (Authentication)
- Flask-WTF / WTForms (Forms)
- Flask-RESTful (REST API)
- SQLite Database

**Frontend:**
- HTML5 with Jinja2 templates
- Bootstrap 5.1.3
- Chart.js
- JavaScript (ES6)

## Project Structure

```
QNA/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── utils.py             # Utility functions
│   ├── admin/               # Admin blueprint
│   │   ├── routes.py        # Admin CRUD operations
│   │   └── forms.py         # Admin forms
│   ├── auth/                # Authentication blueprint
│   │   ├── routes.py        # Login/registration
│   │   └── forms.py         # Auth forms
│   ├── user/                # User blueprint
│   │   ├── routes.py        # User dashboard & quiz taking
│   │   └── forms.py         # User forms
│   ├── api/                 # REST API
│   │   ├── core.py          # API setup
│   │   └── resource.py      # Subject endpoints
│   ├── static/              # CSS, JS, images
│   └── templates/           # HTML templates
├── instance/
│   └── qna.db              # SQLite database
├── config.py               # App configuration
├── requirements.txt        # Python dependencies
└── run.py                  # Application entry point
```

## Installation

### Prerequisites
- Python 3.12 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd QNA
```

2. Create and activate virtual environment:
```bash
python -m venv .env
# Windows
.env\Scripts\activate
# Linux/Mac
source .env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python run.py
```

5. Access the application at `http://localhost:5000`

## Default Credentials

### Quiz Master (Admin)
- Username: `quizmaster`
- Password: `123`

### Users
Register new user accounts via the registration page at `/register`

## Database Models

- **User** - User accounts (admin and regular users)
- **Subject** - Academic subjects
- **Chapter** - Subject subdivisions
- **Quiz** - Quiz definitions with time limits
- **Question** - Multiple choice questions (4 options)
- **QuizAttempt** - Tracks user quiz attempts
- **UserAnswer** - Individual question responses

## API Endpoints

### Subjects API
- `GET /api/subjects` - List all subjects
- `POST /api/subjects` - Create new subject
- `GET /api/subjects/<id>` - Get subject details
- `PUT /api/subjects/<id>` - Update subject
- `DELETE /api/subjects/<id>` - Delete subject

## Configuration

Key settings in `config.py`:
- `SECRET_KEY` - Flask secret key for sessions
- `SQLALCHEMY_DATABASE_URI` - Database connection string
- Default admin credentials

## Security Features

- Password hashing with Werkzeug
- Login required decorators
- Admin-only route protection
- CSRF protection with Flask-WTF
- Session management with Flask-Login

## Development

The application runs in debug mode by default via `run.py`. The database is automatically created in the `instance/` folder on first run.

### Key Routes

**Authentication:**
- `/` - Home/Landing page
- `/login` - User login
- `/register` - User registration
- `/quizmaster/login` - Admin login
- `/logout` - Logout

**Admin:**
- `/admin/dashboard` - Admin dashboard
- `/admin/subjects` - Subject management
- `/admin/quizzes` - Quiz management
- `/admin/users` - User management

**User:**
- `/user/dashboard` - User dashboard
- `/user/quiz/<id>` - Take quiz
- `/user/results/<attempt_id>` - View quiz results
- `/user/profile` - User profile

## License

This project is provided as-is for educational purposes.
