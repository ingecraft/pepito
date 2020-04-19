from sqlalchemy.types import Enum

from db import db

frequencies = ('Annual', 'Monthly', 'Once Off')
frequencies_enum = Enum(*frequencies, name="frequencies")


class DonationModel(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(frequencies_enum)
    amount = db.Column(db.Float(precision=2))
    date_created = db.Column(db.DateTime)

    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    lead = db.relationship('LeadModel')

    operator_id = db.Column(db.Integer, db.ForeignKey('operators.id'))
    operator = db.relationship('OperatorModel')

    def __init__(self, frequency, amount, date_created, lead_id, operator_id):
        self.frequency = frequency
        self.amount = amount
        self.date_created = date_created
        self.lead_id = lead_id
        self.operator_id = operator_id

    @classmethod
    def find_by_id(cls, _id):
        donation = cls.query.filter_by(id=_id).first()
        return donation

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'frequency': self.frequency, 'amount': self.amount,
                'date_created': self.date_created, 'lead_id': self.lead_id,
                'operator_id': self.operator_id}
