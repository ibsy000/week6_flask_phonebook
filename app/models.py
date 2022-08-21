from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True) # it would be cool if when an existing name is entered it would prompt "update current" or "create new"
    phone_number = db.Column(db.String(15), nullable=False)
    street_address = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # lowercase 'user' because that is the name of the table, user.id because id is the column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # SQL Equivalent = FOREIGN KEY(user_id) REFERENCES user(id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Entry {self.id} | {self.name}>"


    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'name', 'phone_number', 'street_address', 'city', 'state', 'email'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    entries = db.relationship('Entry', backref='owner', lazy='dynamic')
    # this creates relationship between the many table that has the foreign key
    # db.relationship('Method', backref='name' --references user.id, always lazy)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Save the password as the hashed version of the password
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id} | {self.username}>"

    # this is used when the password matches the password in the db to that user
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # this takes in the user created password and hashes it for security
    def set_password(self, password):
        self.password = generate_password_hash(password)



@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)
