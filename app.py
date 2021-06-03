from inspect import formatannotation
from flask import render_template, redirect, flash, request, url_for, abort
from flask_wtf.recaptcha.validators import RECAPTCHA_ERROR_CODES
from myproject.forms import (LoginForm, RegistrationForm, AskForm, AnswerForm, 
                                EditForm, RequestResetForm, ResetPasswordForm,
                                ChangePassword)
from flask_login import login_user, login_required, logout_user, current_user
from myproject.models import User, Question
from datetime import datetime
from myproject import app, mail, db
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash


def delta(date):
    diff = datetime.now() - date
    if diff.days:
        if diff.days < 31:
            return f"{diff.days}d ago"
        else:
            return f"{diff.days//30}m ago"
    else:
        if diff.seconds < 60:
            return f"{diff.seconds}sec ago"
        elif diff.seconds > 60 and diff.seconds < 3600:
            return f"{diff.seconds//60}min ago"
        else:
            return f"{diff.seconds//3600}hr ago"


@app.route('/')
@login_required
def home():
    questions = Question.query.filter_by(resolved=False)
    return render_template('home.html', questions=questions, delta=delta, User=User)


@app.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = AskForm()

    if form.validate_on_submit():
        question = Question(question=form.question.data, title=form.title.data, asked_by=current_user.id,
                            answered_by=0,  answer=None, time_asked=datetime.now(), time_answered=None)
        question.save()

        flash('You will be notified when your question gets answered.')
        return redirect(url_for('ask'))

    return render_template('ask.html', form=form)


@app.route('/myquestions', methods=['GET', 'POST'])
@login_required
def myquestions():
    myquestions = Question.query.filter_by(asked_by=current_user.id)
    if request.method == 'POST':
        if request.form.get('resolve'):
            question = Question.query.get(request.form['resolve']) 
            question.resolved = True
            question.save()
        elif request.form.get('unresolve'):
            question = Question.query.get(request.form['unresolve'])
            question.resolved = False
            question.save()


    return render_template('myquestions.html', myquestions=myquestions, User=User, delta=delta)


@app.route('/answer/<int:id>', methods=['GET', 'POST'])
@login_required
def answer(id):
    form = AnswerForm()
    question = Question.query.get(id)
    if question.resolved:
        abort(404)

    if form.validate_on_submit():
        question.answered_by = current_user.id
        question.answer = form.answer.data
        question.time_answered = datetime.now()
        question.resolved = True
        question.save()

        return redirect(url_for('home'))

    return render_template('answer.html', form=form, question=question)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    question = Question.query.get(id)
    if question.asked_by != current_user.id:
        abort(404)
    
    form = EditForm(title=question.title, question=question.question)
    """form.title.data = question.title
    form.question.data = question.question"""
    
    if form.validate_on_submit():
        question.title = form.title.data
        question.question = form.question.data
        question.save()

        return redirect(url_for('myquestions'))
    
    return render_template('edit.html', form=form, question=question)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin.html', Question=Question, User=User)


@app.route('/user/delete/<int:id>')
@login_required
def delete_user(id):
    if id == current_user.id or current_user.role =='Teacher':
        user = User.query.get(id)
        user.delete()

        return redirect(url_for('home'))
    else:
        abort(403)


@app.route('/question/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_question(id):
    question = Question.query.get(id)
    if question.asked_by == current_user.id or current_user.role in ['Admin', 'Teacher']:
        question.delete()

        return redirect(url_for('myquestions'))
    
    else:
        abort(403)


@app.route('/change_password', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePassword()
    user = User.query.get(current_user.id)
    if form.validate_on_submit():
        if check_password_hash(user.password, form.cur_password.data):
            user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'info')
            return redirect(url_for('home'))
        else:
            flash('Incorrect Password!', 'error')
        
    return render_template('change_pwd.html', form=form)
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        if form.password_validate():
            login_user(User.query.filter_by(email=form.email.data).first(), 
                                            remember=form.remember.data)

            next = request.args.get('next')

            if next == None or next[0] != '/':
                next = url_for('home')

            return redirect(next)

        else:
            flash('Incorrect email or password.')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message(
                    'Password Reset Request', 
                    sender='noreply@queue.com',
                    recipients=[user.email],
                    body= f"""To reset your password, visit the following link:
                    {url_for('reset_password', token=token, _external=True)}
                If you did not make this request then simply ignore this email."""
                    )
    print(user.email)
    print(message.body)
    mail.send(message)


@app.route('/reset_password', methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email with instructions to reset your password has been sent', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or expired token!', 'warning')
        return redirect(url_for('request_reset'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in")

        return redirect(url_for('login'))


    return render_template('reset_password.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, fname=form.fname.data.capitalize(),
                    lname=form.lname.data.capitalize(), password=form.password.data, role='Student')
        user.save()

        flash("Thank you for registering")

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('home'))


@app.errorhandler(403)
def error_403(e):
    return render_template('403.html')

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)