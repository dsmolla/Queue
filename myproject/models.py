from myproject import db, login_manager, app
from werkzeug.security import generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.Text)
    lname = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    role = db.Column(db.Text)

    def __init__(self, email, fname, lname, password, role='Student'):
        self.email = email
        self.fname = fname
        self.lname = lname
        self.password = generate_password_hash(password)
        self.role = role
    
    def get_reset_token(self, expires=300):
        s = Serializer(app.secret_key, expires_in=expires)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(id):
        db.session.delete(id)
        db.session.commit()
        
    def __repr__(self):
        return f""" id: {self.id}\n
                    Name: {self.fname} {self.lname}\n
                    email: {self.email}\n
                    role: {self.role}"""

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @staticmethod
    def name(id):
        user = User.query.get(id)
        return f"{user.fname} {user.lname}"


class Question(db.Model):

    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    title = db.Column(db.Text)
    asked_by = db.Column(db.Integer)
    answered_by = db.Column(db.Integer)
    answer = db.Column(db.Text)
    time_asked = db.Column(db.DateTime)
    time_answered = db.Column(db.DateTime)
    resolved = db.Column(db.Boolean)

    def __init__(self, question, title, asked_by, answered_by, answer, time_asked, time_answered, resolved=False):
        self.question = question
        self.title = title
        self.asked_by = asked_by
        self.answered_by = answered_by
        self.answer = answer
        self.time_asked = time_asked
        self.time_answered = time_answered
        self.resolved = resolved

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()