from flask import Flask
from flask_restful import Api

from config import config
from db import db
from resources.operator import Operator, OperatorList

app = Flask(__name__)
app.config.from_object(config['development'])


@app.before_first_request
def create_tables():
    db.create_all()


api = Api(app)

db.init_app(app)

api.add_resource(Operator, '/operators/<string:username>')
api.add_resource(OperatorList, '/operators')


if __name__ == "__main__":
    app.run(port=5000)
