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


class DonationGetCase(BaseCase):
    def test_get_donation_with_non_existing_id_response(self):
        response = self.client.get('/donations/1')

        self.assertEqual(response.json['message'],
                         'There is no donation with this id')

    def test_get_donation_with_non_existing_id_status(self):
        response = self.client.get('/donations/1')

        self.assertEqual(response.status_code, 404)

    def test_get_donation_with_existing_id_json(self):
        donation = create_donation()

        response = self.client.get("/donations/{}".format(donation.id))
        self.assertEqual(response.json, donation.json())

    def test_get_with_existing_id_status(self):
        donation = create_donation()

        response = self.client.get("/donations/{}".format(donation.id))
        self.assertEqual(response.status_code, 200)


class DonationDeleteCase(BaseCase):
    def test_delete_post_with_non_existing_id_json(self):
        response = self.client.delete('/donations/8')

        self.assertEqual(response.json,
                         {'message': 'There is no donation with this id'})

    def test_delete_post_with_non_existing_id_status(self):
        response = self.client.delete('/donations/8')

        self.assertEqual(response.status_code, 404)

    def test_delete_post_with_existing_id_json(self):
        donation = create_donation()

        response = self.client.delete("/donations/{}".format(donation.id))

        self.assertEqual(response.json, {'message': 'Donation deleted'})

    def test_delete_post_with_existing_id_status(self):
        donation = create_donation()

        response = self.client.delete("/donations/{}".format(donation.id))

        self.assertEqual(response.status_code, 200)


class AppealPutCase(BaseCase):
    def test_put_with_no_existing_id_json(self):
        data = {}

        response = self.client.put("donations/2", data=data)
        self.assertEqual(response.json,
                         {'message': 'There is no donation with this id'})

    def test_put_with_no_existing_id_status(self):
        data = {}

        response = self.client.put('/donations/2', data=data)
        self.assertEqual(response.status_code, 404)

    def test_put_with_existing_id_json(self):
        data = {'frequency': 'Monthly'}

        donation = create_donation()

        response = self.client.put("/donations/{}".format(donation.id),
                                   data=data)
        self.assertEqual(response.json,
                         {'id': donation.id, 'frequency': 'Monthly',
                          'amount': 30.00,
                          'operator_id': donation.operator.id,
                          'lead_id': donation.lead.id})

    def test_put_with_existing_id_status(self):
        data = {'frequency': 'Monthly'}

        donation = create_donation()

        response = self.client.put("/donations/{}".format(donation.id),
                                   data=data)
        self.assertEqual(response.status_code, 200)
