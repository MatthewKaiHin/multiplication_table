from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FieldList
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class QuizForm(FlaskForm):
    answer1 = IntegerField('Answer')
    answer2 = IntegerField('Answer')
    answer3 = IntegerField('Answer')
    answer4 = IntegerField('Answer')
    answer5 = IntegerField('Answer')
    ###score = IntegerField('Score')
    submit = SubmitField('Submit')