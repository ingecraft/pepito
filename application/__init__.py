from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    api = Api(app)

    with app.app_context():
        from application.resources.operator import Operator, OperatorList
        from application.resources.lead import Lead, LeadList
        from application.resources.call import Call, CallList
        from application.resources.appeal import Appeal, AppealList
        from application.resources.donation import Donation, DonationList

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
