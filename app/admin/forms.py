from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Email
from app.models import Chapter, Subject
class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    teacher_id = SelectField('Assign Teacher', coerce=int, validators=[Optional()])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        from app.models import Teacher
        self.teacher_id.choices = [(0, '-- No Teacher --')] + [
            (t.id, t.name) for t in Teacher.query.order_by(Teacher.name).all()
        ]

class QuizForm(FlaskForm):
    name = StringField('Quiz Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    time_limit = IntegerField('Time Limit (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    chapter_id = SelectField('Chapter', coerce=int, validators=[Optional()], choices=[], validate_choice=False)
    sequence_number = IntegerField('Sequence Number', validators=[DataRequired(), NumberRange(min=1)], default=1)
    max_attempts = IntegerField('Maximum Attempts', validators=[DataRequired(), NumberRange(min=1, max=10)], default=2)
    passing_score = IntegerField('Passing Score (%)', validators=[DataRequired(), NumberRange(min=0, max=100)], default=70)
    deadline = DateTimeField('Deadline (Optional)', format='%Y-%m-%d %H:%M', validators=[Optional()])
    prerequisite_quiz_id = SelectField('Prerequisite Quiz', coerce=int, validators=[Optional()], choices=[], validate_choice=False)
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        if 'subject_id' in kwargs:
            subject = Subject.query.get(kwargs['subject_id'])
            if subject:
                self.chapter_id.choices = [(0, '-- No Chapter --')] + [
                    (c.id, c.name) for c in subject.chapters
                ]
                self.prerequisite_quiz_id.choices = [(0, '-- No Prerequisite --')] + [
                    (q.id, f"{q.name} (Seq: {q.sequence_number})") for q in subject.quizzes
                ]

class QuestionForm(FlaskForm):
    text = TextAreaField('Question Text', validators=[DataRequired()])
    marks = IntegerField('Marks', validators=[DataRequired(), NumberRange(min=1)], default=1)
    option1 = StringField('Option 1', validators=[DataRequired(), Length(max=200)])
    option2 = StringField('Option 2', validators=[DataRequired(), Length(max=200)])
    option3 = StringField('Option 3', validators=[DataRequired(), Length(max=200)])
    option4 = StringField('Option 4', validators=[DataRequired(), Length(max=200)])
    correct_option = SelectField('Correct Option', 
                               choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')], 
                               coerce=int, 
                               validators=[DataRequired()])
    submit = SubmitField('Save')

class ChapterForm(FlaskForm):
    name = StringField('Chapter Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

class TeacherForm(FlaskForm):
    name = StringField('Teacher Name', validators=[DataRequired(), Length(max=100)])
    qualifications = StringField('Qualifications', validators=[Length(max=200)])
    degree = StringField('Degree', validators=[Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    bio = TextAreaField('Biography')
    submit = SubmitField('Save')