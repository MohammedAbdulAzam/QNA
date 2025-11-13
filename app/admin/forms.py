from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from app.models import Chapter, Subject
class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

class QuizForm(FlaskForm):
    name = StringField('Quiz Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    time_limit = IntegerField('Time Limit (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    chapter_id = SelectField('Chapter', coerce=int, validators=[Optional()], choices=[], validate_choice=False)
    
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        if 'subject_id' in kwargs:
            subject = Subject.query.get(kwargs['subject_id'])
            self.chapter_id.choices = [(c.id, c.name) for c in subject.chapters]
    submit = SubmitField('Save')

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