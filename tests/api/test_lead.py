from tests.test_template import BaseCase

from application.models.lead import LeadModel
from application.models.appeal import AppealModel


class LeadGetCase(BaseCase):
    @classmethod
    def create_lead(cls):
        appeal = AppealModel('Test Title', 'title.url')
        appeal.save_to_db()

        lead = LeadModel('test@test.com', '1111222233', 'Test',
                         'Tester', appeal.id)
        lead.save_to_db()
        return lead

    def test_get_lead_with_non_existing_id_response(self):
        response = self.client.get('/leads/1')

        self.assertEqual(response.json['message'],
                         'There is no lead with this email')

    def test_get_lead_with_non_existing_id_status(self):
        response = self.client.get('/leads/1')

        self.assertEqual(response.status_code, 404)

    def test_get_with_existing_id_json(self):
        lead = self.create_lead()
        _id = lead.json()['id']

        response = self.client.get("/leads/{}".format(_id))
        self.assertEqual(response.json, lead.json())

    def test_get_with_existing_id_status(self):
        lead = self.create_lead()
        _id = lead.json()['id']

        response = self.client.get("/leads/{}".format(_id))
        self.assertEqual(response.status_code, 200)


class AppealDeleteCase(BaseCase):
    @classmethod
    def create_lead(cls):
        appeal = AppealModel('Test Title', 'title.url')
        appeal.save_to_db()

        lead = LeadModel('test@test.com', '1111222233', 'Test',
                         'Tester', appeal.id)
        lead.save_to_db()
        return lead

    def test_delete_post_with_non_existing_id_json(self):
        response = self.client.delete('/leads/8')

        self.assertEqual(response.json,
                         {'message': 'There is no lead with this email'})

    def test_delete_post_with_non_existing_id_status(self):
        response = self.client.delete('/leads/8')

        self.assertEqual(response.status_code, 404)

    def test_delete_post_with_existing_id_json(self):
        lead = self.create_lead()
        _id = lead.json()['id']

        response = self.client.delete("/leads/{}".format(_id))

        self.assertEqual(response.json, {'message': 'Lead deleted'})

    def test_delete_post_with_existing_id_status(self):
        lead = self.create_lead()
        _id = lead.json()['id']

        response = self.client.delete("/leads/{}".format(_id))

        self.assertEqual(response.status_code, 200)


class AppealPutCase(BaseCase):
    @classmethod
    def create_lead(cls):
        appeal = AppealModel('Test Title', 'title.url')
        appeal.save_to_db()

        lead = LeadModel('test@test.com', '1111222233', 'Test',
                         'Tester', appeal.id)
        lead.save_to_db()
        return lead

    def test_put_with_no_existing_id_json(self):
        data = {}

        response = self.client.put("leads/2", data=data)
        self.assertEqual(response.json,
                         {'message': 'There is no lead with this id'})

    def test_put_with_no_existing_id_status(self):
        data = {}

        response = self.client.put('/leads/2', data=data)
        self.assertEqual(response.status_code, 404)

    def test_put_with_existing_id_json(self):
        data = {'name': 'updated'}

        lead = self.create_lead()
        _id = lead.json()['id']

        response = self.client.put("/leads/{}".format(_id),
                                   data=data)
        self.assertEqual(response.json,
                         {'id': _id, 'email': 'test@test.com',
                          'phone': '1111222233', 'name': 'updated',
                          'surname': 'Tester', 'appeal': lead.appeal.json(),
                          'calls': []})

    def test_put_with_existing_id_status(self):
        data = {'url': 'updated'}

        lead = self.create_lead()
        _id = lead.json()['id']

        response = self.client.put("/leads/{}".format(_id),
                                   data=data)
        self.assertEqual(response.status_code, 200)
