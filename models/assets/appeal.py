from db import db


class Appeal(db.Model):
    __tablename__ = 'appeals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    url = db.Column(db.String(80))

    def __init__(self, _id, title, url):
        self.id = _id
        self.title = title
        self.url = url

    @classmethod
    def get_by_id(cls, _id):
        appeal = cls.query.filter_by(id=_id).first()
        return appeal

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
