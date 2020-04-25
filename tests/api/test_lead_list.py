from application.models.lead import LeadModel
from application.models.appeal import AppealModel

from tests.test_template import BaseCase
from tests.api.test_appeal import AppealGetCase as ap


class LeadListPostCase(BaseCase):
    @classmethod
    def post_test_lead(cls):
        appeal = AppealModel('Test Title', 'title.url')
        appeal.save_to_db()

        lead = LeadModel('test@test.com', '1111222233', 'Test',
                         'Tester', appeal.id)
        lead.save_to_db()
        return lead

    @classmethod
    def create_appeal(cls):
        appeal = ap.create_appeal()
        return appeal

    def test_post_lead_with_required_fields_status(self):
        appeal = self.create_appeal()
        _id = appeal.json()['id']
        print(_id)

        data = {'email': 'test@test.com', 'phone': '1111222233',
                'appeal_id': _id}
        response = self.client.post('/leads', data=data)

        self.assertEqual(response.status_code, 200)

    def test_post_lead_with_required_fields_json(self):
        appeal = self.create_appeal()
        appeal_id = appeal.json()['id']

        data = {'email': 'test@test.com', 'phone': '1111222233',
                'appeal_id': appeal_id}

        response = self.client.post('/leads', data=data)

        lead = LeadModel.query.all()[0]
        _id = lead.id

        self.assertEqual(response.json,
                         {'id': _id, 'email': data['email'],
                          'phone': data['phone'], 'name': None,
                          'surname': None, 'appeal': appeal.json(),
                          'calls': []})

    def test_post_lead_with_no_required_fields_status(self):
        data = {'incorrect_field': 'sss'}
        response = self.client.post('/leads', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_lead_with_no_required_fields_json(self):
        data = {'incorrect_field': 'sss'}
        response = self.client.post('/leads', data=data)
        self.assertEqual(response.json,
                         {'message': {'email': 'Email is required'}})

    def test_post_existing_lead_json(self):
        lead = self.post_test_lead()
        email = lead.email

        data = {'email': email, 'phone': '12222222', 'appeal_id': 1}
        response = self.client.post('/leads', data=data)

        self.assertEqual(response.json,
                         {'message':
                          'There is already a lead with this email'})

    def test_post_existing_lead_status(self):
        lead = self.post_test_lead()
        email = lead.email
        data = {'email': email}
        response = self.client.post('/leads', data=data)
        self.assertEqual(response.status_code, 400)


class OperatorListGetCase(BaseCase):
    @classmethod
    def post_test_lead(cls):
        appeal = AppealModel('Test Title', 'title.url')
        appeal.save_to_db()

        lead = LeadModel('test@test.com', '1111222233', 'Test',
                         'Tester', appeal.id)
        lead.save_to_db()
        return lead

    def test_get_no_leads_json(self):
        response = self.client.get('/leads')

        self.assertEqual(response.json, {'leads': []})

    def test_get_no_leads(self):
        response = self.client.get('/appeals')

        self.assertEqual(response.status_code, 200)

    def test_get_one_lead_json(self):
        lead = self.post_test_lead()

        response = self.client.get('/leads')

        self.assertEqual(response.json,
                         {'leads': [lead.json()]})

    def test_get_one_lead_status(self):
        self.post_test_lead()

        response = self.client.get('/leads')
        self.assertEqual(response.status_code, 200)
