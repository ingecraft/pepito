import os
import sys
import click

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


COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='application/*')
    COV.start()


@app.cli.command()
@click.option('--coverage/--nocoverage', default=False,
              help='Run tests under code coverage')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file//%s/index.html' % covdir)
        COV.erase()
