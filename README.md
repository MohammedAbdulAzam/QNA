# QNA - Quiz Management System

A comprehensive full-stack web application for creating, managing, and taking quizzes with advanced features including teacher management, sequential quiz unlocking, attempt limits, and detailed performance tracking.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Security](#security)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🎓 Teacher Management
- **Teacher Profiles** - Store teacher information including name, qualifications, and degree
- **Subject Assignment** - Assign teachers to specific subjects/modules
- **Credential Display** - Show teacher credentials on subject pages for transparency
- **CRUD Operations** - Full management interface for teacher records

### 📚 For Quiz Masters (Admins)

**Content Management:**
- Complete CRUD operations for subjects, chapters, quizzes, and questions
- Teacher management and assignment
- Multiple-choice question creation with 4 options
- Quiz sequencing and prerequisite configuration

**Quiz Control:**
- Set quiz sequence numbers for ordering
- Configure attempt limits (default: 2 attempts)
- Set passing scores for unlocking next quizzes (default: 70%)
- Add optional deadlines for time-sensitive assessments
- Set quiz prerequisites for sequential learning

**Analytics & Monitoring:**
- User management and performance tracking
- Quiz attempt statistics and history
- System-wide analytics with Chart.js visualizations
- Subject-wise performance metrics
- Student progress monitoring

**Search & Organization:**
- Subject search functionality
- Hierarchical content structure (Subjects → Chapters → Quizzes)

### 👨‍🎓 For Students

**Learning Experience:**
- Browse subjects with teacher information
- View module hierarchy (subjects and chapters)
- See clear teacher credentials for each module

**Quiz Taking:**
- Timed multiple-choice quizzes
- Real-time countdown timer with visual feedback
- Automatic submission on timeout
- Clear display of student ID and name during attempts
- Attempt tracking with remaining attempts counter

**Access Control:**
- Sequential quiz unlocking (must pass previous quiz)
- Visual lock indicators for unavailable quizzes
- Clear prerequisite requirements
- Deadline warnings and enforcement
- Attempt limit enforcement

**Performance Tracking:**
- Detailed quiz results with correct/incorrect answers
- Student ID and name on all result pages
- Percentage-based scoring (calculated and displayed)
- Performance dashboard with subject-wise statistics
- Historical attempt tracking
- Interactive charts for visual progress

**Profile Management:**
- Personal profile with age and interests
- Password management
- Performance history

## 🛠 Tech Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.7+ | Core language |
| Flask | 3.1.0 | Web framework |
| SQLAlchemy | Latest | ORM for database |
| Flask-Login | Latest | User authentication |
| Flask-WTF | Latest | Form handling & CSRF protection |
| Flask-RESTful | Latest | REST API endpoints |
| SQLite | Built-in | Database |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| HTML5 | - | Structure |
| Jinja2 | Built-in | Templating |
| Bootstrap | 5.1.3 | UI framework |
| Chart.js | Latest | Data visualization |
| JavaScript | ES6 | Interactivity |

## 📦 Installation

### Quick Setup (Recommended)

#### Windows
```batch
# Run the setup script
setup.bat

# Start the application
run.bat
```

#### Linux/Mac
```bash
# Make scripts executable
chmod +x setup.sh run.sh

# Run the setup script
./setup.sh

# Start the application
./run.sh
```

### Manual Setup

#### Prerequisites
- Python 3.7 or higher
- pip package manager
- Git (for cloning)

#### Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd QNA
```

2. **Create and activate virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Initialize database:**
```bash
# Option 1: Run migration script
python migrate_database.py

# Option 2: Let the app create it automatically
python run.py
```

5. **Access the application:**
```
http://localhost:5000
```

## 🚀 Usage

### Starting the Application

**Using Scripts:**
```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

**Manual Start:**
```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run the application
python run.py
```

### Default Credentials

**Quiz Master (Admin):**
- Username: `quizmaster`
- Password: `123`

**Creating Student Accounts:**
- Navigate to `/register`
- Fill in the registration form
- Login with new credentials

### Admin Workflow

1. **Add Teachers:**
   - Navigate to "Teachers" menu
   - Click "Add Teacher"
   - Fill in name, qualifications, and degree
   - Submit form

2. **Create Subjects:**
   - Go to Dashboard
   - Click "Add New Subject"
   - Assign a teacher from dropdown
   - Add description

3. **Create Quizzes:**
   - Open a subject
   - Click "Add Quiz"
   - Set:
     - Sequence number (1, 2, 3...)
     - Time limit
     - Max attempts (default: 2)
     - Passing score (default: 70%)
     - Deadline (optional)
     - Prerequisite quiz (optional)
   - Submit

4. **Add Questions:**
   - Open a quiz
   - Click "Add Question"
   - Enter question text
   - Add 4 options
   - Select correct option
   - Set marks

### Student Workflow

1. **Browse Subjects:**
   - View available subjects on dashboard
   - See teacher information for each subject
   - Click subject to view details

2. **Take Quizzes:**
   - Navigate to subject → quizzes
   - Check quiz status:
     - 🔓 Unlocked - Can attempt
     - 🔒 Locked - Complete prerequisite first
     - ⏰ Deadline shown if active
     - 🔢 Attempts remaining displayed
   - Click "Attempt" if available
   - Answer questions within time limit
   - Submit or auto-submit on timeout

3. **View Results:**
   - See score percentage
   - View student ID and name
   - Review correct/incorrect answers
   - Check performance dashboard

## 🗄 Database Schema

### Core Models

**User**
- `id` (PK) - Unique identifier (displayed as Student ID)
- `username` - Login username (displayed as Student Name)
- `password_hash` - Hashed password
- `is_admin` - Admin flag
- `age` - Student age
- `interests` - Student interests
- `created_at` - Account creation date

**Teacher** ⭐ New
- `id` (PK) - Unique identifier
- `name` - Teacher's full name
- `qualifications` - Academic qualifications (e.g., "M.Sc., Ph.D.")
- `degree` - Highest degree (e.g., "Ph.D. in Computer Science")
- `email` - Contact email
- `bio` - Brief biography
- `created_at` - Record creation date

**Subject**
- `id` (PK) - Unique identifier
- `name` - Subject name
- `description` - Subject description
- `teacher_id` (FK) ⭐ New - Reference to Teacher
- `created_at` - Creation date

**Quiz**
- `id` (PK) - Unique identifier
- `name` - Quiz name
- `description` - Quiz description
- `time_limit` - Duration in minutes
- `subject_id` (FK) - Reference to Subject
- `chapter_id` (FK) - Optional chapter reference
- `sequence_number` (Integer) ⭐ New - Quiz order (1, 2, 3...)
- `max_attempts` (Integer) ⭐ New - Attempt limit (default: 2)
- `passing_score` (Float) ⭐ New - Pass percentage (default: 70.0)
- `deadline` (DateTime) ⭐ New - Optional due date
- `prerequisite_quiz_id` (FK) ⭐ New - Required previous quiz
- `created_at` - Creation date

**QuizAttempt**
- `id` (PK) - Unique identifier
- `user_id` (FK) - Reference to User
- `quiz_id` (FK) - Reference to Quiz
- `score` (Float) - Percentage score (0-100)
- `completed` (Boolean) - Completion status
- `started_at` - Start timestamp
- `completed_at` - Completion timestamp

### Relationships

```
Teacher (1) ──────< (Many) Subject
Subject (1) ──────< (Many) Chapter
Subject (1) ──────< (Many) Quiz
Chapter (1) ──────< (Many) Quiz
Quiz (1) ──────< (Many) Question
Quiz (1) ──────< (Many) QuizAttempt
Quiz (1) ──────< (Many) Quiz (prerequisite)
User (1) ──────< (Many) QuizAttempt
QuizAttempt (1) ──────< (Many) UserAnswer
Question (1) ──────< (Many) UserAnswer
```

## 🔌 API Documentation

### Subjects API

#### List All Subjects
```http
GET /api/subjects
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Mathematics",
    "description": "Advanced mathematics course",
    "teacher_id": 1,
    "created_at": "2025-01-01T00:00:00"
  }
]
```

#### Get Subject Details
```http
GET /api/subjects/{id}
```

**Response:**
```json
{
  "id": 1,
  "name": "Mathematics",
  "description": "Advanced mathematics course",
  "teacher": {
    "name": "Dr. John Smith",
    "qualifications": "Ph.D., M.Sc.",
    "degree": "Ph.D. in Mathematics"
  },
  "quiz_count": 5
}
```

#### Create Subject
```http
POST /api/subjects
Content-Type: application/json
```

**Body:**
```json
{
  "name": "Physics",
  "description": "Introduction to Physics",
  "teacher_id": 2
}
```

#### Update Subject
```http
PUT /api/subjects/{id}
Content-Type: application/json
```

#### Delete Subject
```http
DELETE /api/subjects/{id}
```

## ⚙ Configuration

### Environment Variables

Create a `.env` file (optional):
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=sqlite:///qna.db
```

### Config File (`config.py`)

```python
class Config:
    SECRET_KEY = 'dev-secret-key-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///qna.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Default Admin Credentials
    QUIZMASTER_USERNAME = 'quizmaster'
    QUIZMASTER_PASSWORD = '123'

    # Quiz Defaults
    DEFAULT_MAX_ATTEMPTS = 2
    DEFAULT_PASSING_SCORE = 70.0
    DEFAULT_QUIZ_SEQUENCE = 1
```

### Database Configuration

**SQLite** (Default):
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///qna.db'
```

**PostgreSQL** (Production):
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/qna'
```

**MySQL**:
```python
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/qna'
```

## 🔒 Security

### Authentication & Authorization
- **Password Hashing:** Werkzeug's `generate_password_hash` and `check_password_hash`
- **Session Management:** Flask-Login for secure user sessions
- **Login Required:** Decorators on protected routes
- **Role-Based Access:** Separate admin and user route protection

### CSRF Protection
- Flask-WTF provides CSRF tokens for all forms
- All POST requests validated

### Access Control
- Admin-only routes return 403 for regular users
- Quiz access validated (unlocked, deadline, attempts)
- User can only access their own data

### Best Practices
- Environment variables for sensitive data
- No passwords in version control
- SQL injection prevention via ORM
- XSS protection via Jinja2 auto-escaping

## 📁 Project Structure

```
QNA/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models (User, Subject, Teacher, Quiz, etc.)
│   ├── utils.py                 # Utility functions (score calculation, etc.)
│   │
│   ├── admin/                   # Admin Blueprint
│   │   ├── __init__.py
│   │   ├── routes.py            # Admin CRUD operations & teacher management
│   │   └── forms.py             # Admin forms (TeacherForm, SubjectForm, QuizForm)
│   │
│   ├── auth/                    # Authentication Blueprint
│   │   ├── __init__.py
│   │   ├── routes.py            # Login, register, logout
│   │   └── forms.py             # LoginForm, RegistrationForm
│   │
│   ├── user/                    # User Blueprint
│   │   ├── __init__.py
│   │   ├── routes.py            # Dashboard, quiz taking, performance
│   │   └── forms.py             # ProfileForm, QuizAnswerForm
│   │
│   ├── api/                     # REST API
│   │   ├── __init__.py
│   │   ├── core.py              # API initialization
│   │   └── resource.py          # Subject API endpoints
│   │
│   ├── static/                  # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   └── images/
│   │       └── logo.png
│   │
│   └── templates/               # Jinja2 templates
│       ├── base.html            # Base template
│       ├── includes/
│       │   └── _header.html     # Navigation header
│       ├── admin/               # Admin templates
│       │   ├── dashboard.html
│       │   ├── teachers.html    # ⭐ New
│       │   ├── add_teacher.html # ⭐ New
│       │   ├── view_subject.html
│       │   └── ...
│       ├── user/                # User templates
│       │   ├── dashboard.html
│       │   ├── view_quizzes.html
│       │   ├── attempt_quiz.html
│       │   ├── quiz_result.html
│       │   └── ...
│       └── auth/                # Auth templates
│           ├── login.html
│           └── register.html
│
├── migrations/                  # Database migrations
│   └── add_teacher_and_quiz_rules.py
│
├── instance/
│   └── qna.db                  # SQLite database (created automatically)
│
├── config.py                   # Application configuration
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── migrate_database.py         # Database migration script
├── MIGRATION_INSTRUCTIONS.md   # Migration guide
│
├── setup.sh                    # Linux/Mac setup script ⭐ New
├── setup.bat                   # Windows setup script ⭐ New
├── run.sh                      # Linux/Mac run script ⭐ New
├── run.bat                     # Windows run script ⭐ New
│
└── README.md                   # This file
```

## 🎯 Key Features Explained

### Sequential Quiz Unlocking

Quizzes can be configured to unlock sequentially:

1. **Setup (Admin):**
   - Quiz 1: No prerequisite (always available)
   - Quiz 2: Prerequisite = Quiz 1, Passing Score = 70%
   - Quiz 3: Prerequisite = Quiz 2, Passing Score = 70%

2. **Student Experience:**
   - Quiz 1: ✅ Unlocked
   - Quiz 2: 🔒 Locked (must pass Quiz 1 with ≥70%)
   - Quiz 3: 🔒 Locked (must pass Quiz 2 with ≥70%)

3. **Visual Indicators:**
   - Locked badge for unavailable quizzes
   - Clear prerequisite messages
   - Progress tracking

### Attempt Limiting

Students get limited attempts per quiz (default: 2):

- **Counter Display:** "Attempt (2 left)" → "Attempt (1 left)"
- **Exhausted:** "No attempts remaining" message
- **Tracking:** Only completed attempts count toward limit
- **Incomplete:** Abandoned attempts don't count

### Deadline Management

Optional deadlines for time-sensitive assessments:

- **Before Deadline:** Shows due date, allows attempts
- **After Deadline:** "Deadline Passed" badge, blocks attempts
- **Display:** Clear deadline shown on quiz listing
- **Format:** YYYY-MM-DD HH:MM

### Teacher Display

Teacher information shows on relevant pages:

**Admin View:**
- Teacher management page with all credentials
- Subject edit form with teacher assignment
- Subject view with full teacher details

**Student View:**
- Subject page shows teacher name, qualifications, degree
- Builds trust and transparency
- Professional presentation

### Student Identification

Student ID and Name displayed on:
- Quiz attempt page header
- Quiz result page
- Performance dashboard
- All score displays

This ensures proper student identification and record-keeping.

## 🧪 Testing

### Manual Testing Checklist

**Teacher Management:**
- [ ] Create new teacher
- [ ] Edit teacher details
- [ ] Delete teacher
- [ ] Assign teacher to subject
- [ ] View teacher on subject page

**Quiz Access Control:**
- [ ] Sequential unlocking works
- [ ] Attempt limits enforced
- [ ] Deadline blocks access after expiry
- [ ] Lock indicators display correctly
- [ ] Prerequisite messages accurate

**Student Display:**
- [ ] Student ID shows on all pages
- [ ] Student name shows on all pages
- [ ] Percentage calculates correctly
- [ ] Results page shows full details

### Test User Scenarios

**Scenario 1: Complete Quiz Path**
1. Student attempts Quiz 1
2. Scores 80% (above 70% passing)
3. Quiz 2 unlocks
4. Student attempts Quiz 2
5. Continues to Quiz 3

**Scenario 2: Failed Prerequisite**
1. Student attempts Quiz 1
2. Scores 50% (below 70%)
3. Quiz 2 remains locked
4. Student retries Quiz 1 (1 attempt left)
5. Scores 75% → Quiz 2 unlocks

**Scenario 3: Attempt Exhaustion**
1. Student fails Quiz 1 twice
2. "No attempts remaining" shows
3. Quiz 1 blocked
4. Admin can manually reset if needed

## 🐛 Troubleshooting

### Common Issues

**Database Not Found:**
```bash
# Delete and recreate
rm qna.db
python migrate_database.py
```

**Virtual Environment Issues:**
```bash
# Windows
deactivate
rmdir /s venv
python -m venv venv
venv\Scripts\activate

# Linux/Mac
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

**Flask Not Found:**
```bash
pip install -r requirements.txt
```

**Port Already in Use:**
```python
# Edit run.py, change port:
app.run(debug=True, port=5001)
```

**Quiz Not Unlocking:**
- Check passing score met
- Verify prerequisite quiz ID correct
- Ensure attempt was completed (not abandoned)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Update README for new features
- Test thoroughly before submitting
- Keep commits atomic and descriptive

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## 🙏 Acknowledgments

- Flask documentation and community
- Bootstrap for UI components
- Chart.js for visualizations
- SQLAlchemy for ORM capabilities

## 📈 Roadmap

Future enhancements planned:
- [ ] Email notifications for deadlines
- [ ] Bulk question import (CSV/Excel)
- [ ] Quiz templates and cloning
- [ ] Advanced analytics and reporting
- [ ] Mobile app integration
- [ ] Real-time quiz sessions
- [ ] Gamification features
- [ ] Certificate generation
- [ ] Multi-language support

---

**Made with ❤️ for education**

*Last Updated: December 2025*
