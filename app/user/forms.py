from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    age = IntegerField('Age', validators=[NumberRange(min=1, max=120)])
    interests = TextAreaField('Interests')
    submit = SubmitField('Update Profile')

class QuizAnswerForm(FlaskForm):
    # This will be dynamically generated in the route
    submit = SubmitField('Submit Quiz')