from tests.test_template import BaseCase

from application.models.call import CallModel
from application.models.donation import DonationModel
from application.models.operator import OperatorModel
from application.models.lead import LeadModel
from application.models.appeal import AppealModel


def create_call():
    appeal = AppealModel('title', 'url')
    appeal.save_to_db()

    lead = LeadModel('email', 'phone', 'name', 'surname', appeal.id)
    lead.save_to_db()

    operator = OperatorModel('testuser', 'name', 'surname', 'email')
    operator.save_to_db()

    call = CallModel('04-12-2020', '03::04::05', 5.4, lead.id, operator.id)
    call.save_to_db()


def create_lead_and_operator():
    appeal = AppealModel('title', 'url')
    appeal.save_to_db()

    lead = LeadModel('email', 'phone', 'name', 'surname', appeal.id)
    lead.save_to_db()

    operator = OperatorModel('testuser', 'name', 'surname', 'email')
    operator.save_to_db()

    return lead, operator


class DonationListPostCase(BaseCase):
    def test_post_call_with_required_fields_status(self):
        lead, operator = create_lead_and_operator()

        data = {'date': '04-12-2020', 'time': '03::04::03', 'duration': 5.4,
                'lead_id': lead.id, 'operator_id': operator.id}

        response = self.client.post('/calls', data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_call_with_required_fields_json(self):
        lead, operator = create_lead_and_operator()

        data = {'date': '04-12-2020', 'time': '03::04::03', 'duration': 5.4,
                'lead_id': lead.id, 'operator_id': operator.id}

        response = self.client.post('/calls', data=data)

        call = CallModel.query.all()[0]
        self.assertEqual(response.json,
                         {'id': call.id, 'date': '2020-04-12',
                          'time': '03:04:03', 'duration': 5.4,
                          'lead_id': lead.id, 'operator_id': operator.id})

    def test_post_call_with_no_required_fields_status(self):
        data = {'incorrect_field': 'sss'}
        response = self.client.post('/calls', data=data)
        self.assertEqual(response.status_code, 400)

#    def test_post_call_with_no_required_fields_json(self):
#        data = {'incorrect_field': 'sss'}
#        response = self.client.post('/calls', data=data)
#        self.assertEqual(response.json,
#                         {'message': {'frequency': 'is required'}})
#
#    def test_post_existing_call_json(self):
#        call = create_donation()
#
#        data = {'frequency': 'Annual', 'amount': 30.00,
#                'lead_id': call.lead.id,
#                'operator_id': 3}
#
#        response = self.client.post('/calls', data=data)
#
#        self.assertEqual(response.json,
#                         {'message':
#                          'There is already a call for this lead'})
#
#    def test_post_existing_call_status(self):
#        call = create_donation()
#
#        data = {'frequency': 'Annual', 'amount': 30.00,
#                'lead_id': call.lead.id,
#                'operator_id': 3}
#
#        response = self.client.post('/calls', data=data)
#        self.assertEqual(response.status_code, 400)
#
#
#class OperatorListGetCase(BaseCase):
#    def test_get_no_calls_json(self):
#        response = self.client.get('/calls')
#
#        self.assertEqual(response.json, {'calls': []})
#
#    def test_get_no_calls(self):
#        response = self.client.get('/calls')
#
#        self.assertEqual(response.status_code, 200)
#
#    def test_get_one_call_json(self):
#        call = create_donation()
#
#        response = self.client.get('/calls')
#
#        self.assertEqual(response.json,
#                         {'calls': [donation.json()]})
#
#    def test_get_one_call_status(self):
#        create_call()
#
#        response = self.client.get('/calls')
#        self.assertEqual(response.status_code, 200)
