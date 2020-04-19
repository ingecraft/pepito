from db import db


class LeadModel(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))

    calls = db.relationship('CallModel', lazy='dynamic')

    appeal_id = db.Column(db.Integer, db.ForeignKey('appeals.id'))
    appeal = db.relationship('AppealModel')

    def __init__(self, email, phone, name, surname):
        self.email = email
        self.phone = phone
        self.name = name
        self.surname = surname

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'email': self.email, 'phone': self.phone,
                'name': self.name, 'surname': self.surname,
                'appeal': self.appeal.json(),
                'calls': [call.json() for call in self.calls.all()]}
