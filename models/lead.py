from db import db


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(80))

    def __init__(self, _id, name, surname, phone, email):
        self._id = id
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email

    @classmethod
    def get_by_id(cls, _id):
        lead = cls.query.filter_by(id=_id).first()
        return lead

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
