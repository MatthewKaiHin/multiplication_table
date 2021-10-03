from app import db
from app.models import User

user1 = User(username='AnnChan', email='annchan@multiplication.com', role="Teacher")
user2 = User(username='JoeLam', email='joelam@multiplication.com', role="Student")
user3 = User(username='BobFung', email='bobfung@multiplication.com', role="Student")
user4 = User(username='CandyChoi', email='candychoi@multiplication.com', role="Student")
user5 = User(username='SammyLo', email='sammylo@multiplication.com', role="Student")
user6 = User(username='GigiLau', email='gigilau@multiplication.com', role="Student")


user1.set_password('123456')
user2.set_password('123456')
user3.set_password('123456')
user4.set_password('123456')
user5.set_password('123456')
user6.set_password('123456')

u = [user1, user2, user3, user4, user5, user6]

db.session.add_all(u)

db.session.commit()