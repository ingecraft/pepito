from sqlalchemy.types import Enum

from application.db import db

frequencies = ('Annual', 'Monthly', 'Once Off')
frequencies_enum = Enum(*frequencies, name="frequencies")


class DonationModel(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(frequencies_enum)
    amount = db.Column(db.Float(precision=2))
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())

    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    lead = db.relationship('LeadModel')

    operator_id = db.Column(db.Integer, db.ForeignKey('operators.id'))
    operator = db.relationship('OperatorModel')

    def __init__(self, frequency, amount, lead_id, operator_id):
        self.frequency = frequency
        self.amount = amount
        self.lead_id = lead_id
        self.operator_id = operator_id

    @classmethod
    def find_by_id(cls, _id):
        donation = cls.query.filter_by(id=_id).first()
        return donation

    @classmethod
    def find_by_lead_id(cls, lead_id):
        donation = cls.query.filter_by(lead_id=lead_id).first()
        return donation

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'frequency': self.frequency,
                'amount': self.amount, 'lead_id': self.lead_id,
                'operator_id': self.operator_id}
