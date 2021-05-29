from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    fname = db.Column(db.Text)
    lname = db.Column(db.Text)
    password_hashed = db.Column(db.Text)
    role = db.relationship('Role', backref='user', lazy='dynamic')

    def __init__(self, email, fname, lname, password, role):
        self.email = email
        self.fname = fname
        self.lname = lname
        self.password_hashed = generate_password_hash(password)
        self.role = role

    def password_check(self, password):
        return check_password_hash(self.password_hashed, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"User"


class Question(db.Model):

    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    asked_by = db.Column(db.Integer)
    answered_by = db.Column(db.Integer)
    answer = db.Column(db.Text)
    time_asked = db.Column(db.DateTime)
    time_answered = db.Column(db.DateTime)

    def __init__(self, question, asked_by, answered_by, answer, time_asked, time_answered):
        self.question = question
        self.asked_by = asked_by
        self.answered_by = answered_by
        self.answer = answer
        self.time_asked = time_asked
        self.time_answered = time_answered

    def save(self):
        db.session.add(self)
        db.session.commit()