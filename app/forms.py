from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class QuizForm(FlaskForm):
    userid = SelectMultipleField('Student', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Submit')

class AnswerForm(FlaskForm):
    answer1 = IntegerField('Answer1')
    answer2 = IntegerField('Answer2')
    answer3 = IntegerField('Answer3')
    answer4 = IntegerField('Answer4')
    answer5 = IntegerField('Answer5')
    submit = SubmitField('Submit')