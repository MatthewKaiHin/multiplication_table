from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, QuizForm, AnswerForm
from app.models import User, Quiz, Answer
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import random

def quiz_to_user():
    user_quiz_open = []
    user_choices = []
    for quiz in db.session.query(Quiz).filter_by(stage='open'):
        user_quiz_open.append(quiz.user_id)
    for user in db.session.query(User).filter_by(role='Student'):
        if not user.id in user_quiz_open:
            user_choices.append((user.id, user.username))
    return user_choices

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form=QuizForm()
    form.userid.choices = quiz_to_user()
    if form.validate_on_submit():
        quizzes_total = []
        for select_user in form.userid.data:
            draw = 1
            question_list = []
            answer_list = []
            while draw < 6:
                draw_number_1 = random.randint(1, 10)
                draw_number_2 = random.randint(1, 10)
                question = ('{0} x {1} =').format(draw_number_1, draw_number_2)
                answer = draw_number_1 * draw_number_2
                if question in question_list:
                    draw += 0
                elif not question in question_list:
                    question_list.append(question)
                    answer_list.append(answer)
                    draw += 1
            quizzes = Quiz(user_id=select_user, question1=question_list[0],answer1=answer_list[0],
                           question2=question_list[1], answer2=answer_list[1], question3=question_list[2],
                           answer3=answer_list[2], question4=question_list[3], answer4=answer_list[3],
                           question5=question_list[4], answer5=answer_list[4], stage='open')
            quizzes_total.append(quizzes)
        db.session.add_all(quizzes_total)
        db.session.commit()
        flash('New quizzes created')
        return redirect(url_for('home'))
    quizzes = db.session.query(Quiz).filter_by(stage='open')
    return render_template('home.html', title='Home', form=form, quizzes=quizzes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    quizzes = db.session.query(Quiz).filter_by(id=quiz_id)
    for quiz in db.session.query(Quiz).filter_by(id=quiz_id):
        questions = [quiz.question1, quiz.question2, quiz.question3, quiz.question4, quiz.question5]
    form = AnswerForm()
    if form.validate_on_submit():
        for check in db.session.query(Quiz).filter_by(id=quiz_id):
            score = 0
            if check.answer1 == form.answer1.data:
                score += 1
            elif check.answer2 == form.answer2.data:
                score += 1
            elif check.answer3 == form.answer3.data:
                score += 1
            elif check.answer4 == form.answer4.data:
                score += 1
            elif check.answer5 == form.answer5.data:
                score += 1
        answer = Answer(answer1=form.answer1.data, answer2=form.answer2.data, answer3=form.answer3.data,
                        answer4=form.answer4.data, answer5=form.answer5.data, score=score, quiz_id=quiz_id)
        db.session.add(answer)
        db.session.commit()
        flash('Quiz submited')
        return redirect(url_for('home'))
    return render_template('quiz.html', title='Quiz', quizzes=quizzes,
                           questions=questions, form=form)