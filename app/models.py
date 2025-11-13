from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    age = db.Column(db.Integer)
    interests = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    quiz_attempts = db.relationship(
        'QuizAttempt', 
        backref='user', 
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    quizzes = db.relationship(
        'Quiz', 
        backref='subject', 
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    chapters = db.relationship(
        'Chapter',
        backref='subject',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def __repr__(self):
        return f'<Subject {self.name}>'
    
class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    quizzes = db.relationship(
        'Quiz', 
        backref='chapter', 
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def __repr__(self):
        return f'<Chapter {self.name}>'

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    time_limit = db.Column(db.Integer)  # in minutes
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship(
        'Question', 
        backref='quiz', 
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    attempts = db.relationship(
        'QuizAttempt', 
        backref='quiz', 
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def __repr__(self):
        return f'<Quiz {self.name}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    marks = db.Column(db.Integer, default=1)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)  # 1-4
    quiz_id = db.Column(
        db.Integer, 
        db.ForeignKey('quiz.id', ondelete='CASCADE'), 
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Question {self.text[:50]}...>'

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id', ondelete='CASCADE'), 
        nullable=False
    )
    quiz_id = db.Column(
        db.Integer, 
        db.ForeignKey('quiz.id', ondelete='CASCADE'), 
        nullable=False
    )
    score = db.Column(db.Float, default=0.0)
    completed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    answers = db.relationship(
        'UserAnswer', 
        backref='attempt', 
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def __repr__(self):
        return f'<QuizAttempt {self.user.username} - {self.quiz.name}>'

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(
        db.Integer, 
        db.ForeignKey('quiz_attempt.id', ondelete='CASCADE'), 
        nullable=False
    )
    question_id = db.Column(
        db.Integer, 
        db.ForeignKey('question.id', ondelete='CASCADE'), 
        nullable=False
    )
    selected_option = db.Column(db.Integer)  # 1-4
    is_correct = db.Column(db.Boolean)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    question = db.relationship(
        'Question', 
        backref='user_answers',
        passive_deletes=True
    )

    def __repr__(self):
        return f'<UserAnswer {self.attempt_id} - Q{self.question_id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))