from datetime import datetime

from db import db


class CallModel(db.Model):
    __tablename__ = 'calls'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    duration = db.Column(db.Float(precision=2))

    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    lead = db.relationship('LeadModel')

    operator_id = db.Column(db.Integer, db.ForeignKey('operators.id'))
    operator = db.relationship('OperatorModel')

    def __init__(self, date, time, duration, lead_id, operator_id):
        self.date = datetime.strptime(date, '%m-%d-%Y').date()
        self.time = datetime.strptime(time, '%H::%M::%S').time()
        self.duration = duration
        self.lead_id = lead_id
        self.operator_id = operator_id

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'date': self.date, 'time': self.time,
                'duration': self.duration, 'operator_id': self.operator_id,
                'lead_id': self.lead_id}
