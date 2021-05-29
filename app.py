from flask import render_template, redirect, flash, request, url_for, abort
from myproject.forms import LoginForm, RegistrationForm, AskForm, AnswerForm
from flask_login import login_user, login_required, logout_user, current_user
from myproject.models import User, Question
from datetime import datetime
from myproject import app


@app.route('/')
@login_required
def home():
    myquestions = Question.query.filter_by(asked_by=current_user.id)
    return render_template('home.html', myquestions=myquestions, User=User)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_check(form.password.data):
            login_user(user, remember=form.remember.data)

            next = request.args.get('next')

            if next == None or next[0] != '/':
                next = url_for('home')

            return redirect(next)

        else:
            flash('Incorrect email or password.')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if form.email_exists():
            flash('The email you provided is already registered!')

            return render_template('register.html', form=form)

        user = User(email=form.email.data, fname=form.fname.data.capitalize(),
                    lname=form.lname.data.capitalize(), password=form.password.data)
        user.save()

        flash("Thank you for registering")

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('home'))


@app.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = AskForm()

    if form.validate_on_submit():
        question = Question(question=form.question.data, asked_by=current_user.id,
                            answered_by=0,  answer=None, time_asked=datetime.now(), time_answered=None)
        question.save()

        flash('You will be notified when your question gets answered.')
        return redirect(url_for('ask'))

    return render_template('ask.html', form=form)


@app.route('/question/<int:id>', methods=['GET', 'POST'])
@login_required
def answer(id):
    form = AnswerForm()
    question = Question.query.get(id)
    if question.answered_by:
        abort(404)

    if form.validate_on_submit():
        question.answered_by = current_user.id
        question.answer = form.answer.data
        question.time_answered = datetime.now()
        question.save()

        return redirect(url_for('home'))

    return render_template('answer.html', form=form, question=question.question)


@app.route('/questions')
@login_required
def myquestions():
    unanswered = Question.query.filter_by(answered_by=0)
    return render_template('myquestions.html', unanswered=unanswered)



if __name__ == '__main__':
    app.run(debug=True)