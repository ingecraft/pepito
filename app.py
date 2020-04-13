from flask import Flask
from flask_restful import Api

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'bandit'


@app.before_first_request
def create_tables():
    db.create_all()


api = Api(app)

db.init_app(app)


if __name__ == "__main__":
    app.run(port=5000)
