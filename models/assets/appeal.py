from db import db


class AppealModel(db.Model):
    __tablename__ = 'appeals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    url = db.Column(db.String(80))

    def __init__(self, title, url):
        self.title = title
        self.url = url

    @classmethod
    def find_by_id(cls, _id):
        appeal = cls.query.filter_by(id=_id).first()
        return appeal

    @classmethod
    def find_by_url(cls, url):
        appeal = cls.query.filter_by(url=url).first()
        return appeal

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'title': self.title, 'url': self.url}
