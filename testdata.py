from app import db
from app.models import User, Post

user1 = User(username='AnnChan', email='annchan@multiplication.com', role="Teacher")
user2 = User(username='JoeLam', email='joelam@multiplication.com', role="Student")

user1.set_password('123456')
user2.set_password('123456')

db.session.add(user1)
db.session.add(user2)

db.session.commit()