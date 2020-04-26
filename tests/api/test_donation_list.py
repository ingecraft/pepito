from tests.test_template import BaseCase

from application.models.donation import DonationModel
from application.models.operator import OperatorModel
from application.models.lead import LeadModel
from application.models.appeal import AppealModel


def create_donation():
    appeal = AppealModel('title', 'url')
    appeal.save_to_db()

    lead = LeadModel('email', 'phone', 'name', 'surname', appeal.id)
    lead.save_to_db()

    operator = OperatorModel('testuser', 'name', 'surname', 'email')
    operator.save_to_db()

    donation = DonationModel('Annual', 30.00, lead.id, operator.id)
    donation.save_to_db()
    return donation


def create_lead_and_operator():
    appeal = AppealModel('title', 'url')
    appeal.save_to_db()

    lead = LeadModel('email', 'phone', 'name', 'surname', appeal.id)
    lead.save_to_db()

    operator = OperatorModel('testuser', 'name', 'surname', 'email')
    operator.save_to_db()

    return lead, operator


class DonationListPostCase(BaseCase):
    def test_post_donation_with_required_fields_status(self):
        lead, operator = create_lead_and_operator()

        data = {'frequency': 'Annual', 'amount': 30.00,
                'lead_id': lead.id,
                'operator_id': operator.id}

        response = self.client.post('/donations', data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_donation_with_required_fields_json(self):
        lead, operator = create_lead_and_operator()

        data = {'frequency': 'Annual', 'amount': 30.00,
                'lead_id': lead.id,
                'operator_id': operator.id}

        response = self.client.post('/donations', data=data)

        donation = DonationModel.query.all()[0]

        self.assertEqual(response.json,
                         {'id': donation.id, 'frequency': 'Annual',
                          'amount': 30.00, 'lead_id': lead.id,
                          'operator_id': operator.id})

    def test_post_donation_with_no_required_fields_status(self):
        data = {'incorrect_field': 'sss'}
        response = self.client.post('/donations', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_donation_with_no_required_fields_json(self):
        data = {'incorrect_field': 'sss'}
        response = self.client.post('/donations', data=data)
        self.assertEqual(response.json,
                         {'message': {'frequency': 'Frequency is required'}})

    def test_post_existing_donation_json(self):
        donation = create_donation()

        data = {'frequency': 'Annual', 'amount': 30.00,
                'lead_id': donation.lead.id,
                'operator_id': 3}

        response = self.client.post('/donations', data=data)

        self.assertEqual(response.json,
                         {'message':
                          'There is already a donation for this lead'})

    def test_post_existing_donation_status(self):
        donation = create_donation()

        data = {'frequency': 'Annual', 'amount': 30.00,
                'lead_id': donation.lead.id,
                'operator_id': 3}

        response = self.client.post('/donations', data=data)
        self.assertEqual(response.status_code, 400)


class OperatorListGetCase(BaseCase):
    def test_get_no_donations_json(self):
        response = self.client.get('/donations')

        self.assertEqual(response.json, {'donations': []})

    def test_get_no_donations(self):
        response = self.client.get('/donations')

        self.assertEqual(response.status_code, 200)

    def test_get_one_donation_json(self):
        donation = create_donation()

        response = self.client.get('/donations')

        self.assertEqual(response.json,
                         {'donations': [donation.json()]})

#    def test_get_one_donation_status(self):
#        self.post_test_donation()
#
#        response = self.client.get('/donations')
#        self.assertEqual(response.status_code, 200)
