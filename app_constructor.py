from flask import Flask
from flask_restful import Api

from config import config
from db import db

from resources.people.operator import Operator, OperatorList
from resources.people.lead import Lead, LeadList
from resources.assets.call import Call, CallList
from resources.assets.appeal import Appeal, AppealList
from resources.assets.donation import Donation, DonationList


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    api = Api(app)

    api.add_resource(Operator, '/operators/<int:id>')
    api.add_resource(OperatorList, '/operators')
    api.add_resource(Lead, '/leads/<int:id>')
    api.add_resource(LeadList, '/leads')
    api.add_resource(Call, '/calls/<int:id>')
    api.add_resource(CallList, '/calls')
    api.add_resource(Appeal, '/appeals/<int:id>')
    api.add_resource(AppealList, '/appeals')
    api.add_resource(Donation, '/donations/<int:id>')
    api.add_resource(DonationList, '/donations')

    return app
