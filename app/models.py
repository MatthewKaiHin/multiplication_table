from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(128))
    quizzes = db.relationship('Quiz', backref='examinee', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.String(140))
    answer1 = db.Column(db.Integer)
    question2 = db.Column(db.String(140))
    answer2 = db.Column(db.Integer)
    question3 = db.Column(db.String(140))
    answer3 = db.Column(db.Integer)
    question4 = db.Column(db.String(140))
    answer4 = db.Column(db.Integer)
    question5 = db.Column(db.String(140))
    answer5 = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    stage = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '{}'.format(self.stage)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer1 = db.Column(db.Integer)
    answer2 = db.Column(db.Integer)
    answer3 = db.Column(db.Integer)
    answer4 = db.Column(db.Integer)
    answer5 = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    score = db.Column(db.Integer)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    def __repr__(self):
        return '{}'.format(self.score)
