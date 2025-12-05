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

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    qualifications = db.Column(db.String(200))  # e.g., "M.Sc., Ph.D."
    degree = db.Column(db.String(100))  # e.g., "Ph.D. in Computer Science"
    email = db.Column(db.String(120), unique=True)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    subjects = db.relationship('Subject', backref='teacher', lazy=True)

    def __repr__(self):
        return f'<Teacher {self.name}>'

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='SET NULL'), nullable=True)
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
    sequence_number = db.Column(db.Integer, default=1)
    max_attempts = db.Column(db.Integer, default=2)
    passing_score = db.Column(db.Float, default=70.0)
    deadline = db.Column(db.DateTime, nullable=True)
    prerequisite_quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    prerequisite = db.relationship(
        'Quiz',
        remote_side='Quiz.id',
        backref='dependent_quizzes',
        foreign_keys=[prerequisite_quiz_id]
    )
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

    def is_unlocked_for_user(self, user):
        """Check if quiz is unlocked for given user"""
        if not self.prerequisite_quiz_id:
            return True

        prerequisite_attempts = QuizAttempt.query.filter_by(
            user_id=user.id,
            quiz_id=self.prerequisite_quiz_id,
            completed=True
        ).all()

        for attempt in prerequisite_attempts:
            if attempt.score >= self.prerequisite.passing_score:
                return True
        return False

    def attempts_remaining_for_user(self, user):
        """Return number of attempts remaining"""
        completed_attempts = QuizAttempt.query.filter_by(
            user_id=user.id,
            quiz_id=self.id,
            completed=True
        ).count()
        return max(0, self.max_attempts - completed_attempts)

    def is_past_deadline(self):
        """Check if deadline has passed"""
        if not self.deadline:
            return False
        return datetime.utcnow() > self.deadline

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