import os

from flask_migrate import Migrate

from application import create_app, db
from application.models.lead import LeadModel
from application.models.operator import OperatorModel
from application.models.appeal import AppealModel
from application.models.call import CallModel
from application.models.donation import DonationModel

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, LeadModel=LeadModel, OperatorModel=OperatorModel,
                CallModel=CallModel, DonationModel=DonationModel,
                AppealModel=AppealModel)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
