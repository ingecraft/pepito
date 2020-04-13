from db import db


class Operator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    email = db.Column(db.String(80))

    def __init__(self, username, name, surname, email):
        self.usernam = username
        self.name = name
        self.surname = surname
        self.email = email

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
