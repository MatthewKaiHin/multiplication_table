from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, QuizForm
from app.models import User, Quiz
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import random

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

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

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    form = QuizForm()
    draw = 1
    draw_list = []
    ans_list = []
    if request.method == 'GET':
        while draw < 6:
            draw_number_1 = random.randint(1, 10)
            draw_number_2 = random.randint(1, 10)
            question = ('{0} x {1} =').format(draw_number_1, draw_number_2)
            answer = draw_number_1 * draw_number_2
            if question in draw_list:
                draw += 0
            if not question in draw_list:
                draw_list.append(question)
                ans_list.append(answer)
                draw += 1
    if form.validate_on_submit():
        count_score = 0
        if ans_list[0] == form.answer1.data:
            count_score += 1
        elif ans_list[1] == form.answer2.data:
            count_score += 1
        elif ans_list[2] == form.answer3.data:
            count_score += 1
        elif ans_list[3] == form.answer4.data:
            count_score += 1
        elif ans_list[4] == form.answer5.data:
            count_score += 1
        quizzes = Quiz(question1=draw_list[0],question2=draw_list[1],question3=draw_list[2],
                       question4=draw_list[3],question5=draw_list[4],answer1=form.answer1.data,
                       answer2=form.answer2.data,answer3=form.answer3.data,answer4=form.answer4.data,
                       answer5=form.answer5.data,score=count_score, submitter=current_user)
        db.session.add(quizzes)
        db.session.commit()
        flash('Submited')
        return redirect(url_for('home'))
    return render_template('quiz.html', title='Quiz', draw_list=draw_list,
                           ans_list=ans_list, form=form)