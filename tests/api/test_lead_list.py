from application.models.lead import LeadModel

from tests.test_template import BaseCase
from tests.api.test_appeal import AppealGetCase as ap


class LeadListPostCase(BaseCase):
    @classmethod
    def post_test_lead(cls):
        lead = LeadModel('test@test.com', '1111222233', 'Test',
                         'Tester', 1)
        lead.save_to_db()
        return lead

    @classmethod
    def create_appeal(cls):
        appeal = ap.create_appeal()
        return appeal

    def test_post_lead_with_required_fields_status(self):
        appeal = self.create_appeal()
        _id = appeal.json()['id']

        data = {'email': 'test@test.com', 'phone': '1111222233',
                'appeal_id': _id}
        response = self.client.post('/leads', data=data)

        self.assertEqual(response.status_code, 200)

    def test_post_lead_with_required_fields_json(self):
        appeal = self.create_appeal()
        _id = appeal.json()['id']

        data = {'email': 'test@test.com', 'phone': '1111222233',
                'appeal_id': _id}

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

#    def test_post_existing_appeal_json(self):
#        appeal = self.post_test_appeal()
#        url = appeal.url
#        data = {'url': url}
#        response = self.client.post('/appeals', data=data)
#        self.assertEquals(response.json,
#                          {'message':
#                           'There is already an appeal with this url'})
#
#    def test_post_existing_appeal_status(self):
#        appeal = self.post_test_appeal()
#        url = appeal.url
#        data = {'url': url}
#        response = self.client.post('/appeals', data=data)
#        self.assertEquals(response.status_code, 400)
#
#
#class OperatorListGetCase(BaseCase):
#    def post_test_appeal(self, url):
#        appeal = AppealModel('test', url)
#        appeal.save_to_db()
#
#        return appeal
#
#    def test_get_no_appeals_json(self):
#        response = self.client.get('/appeals')
#
#        self.assertEquals(response.json, {'appeals': []})
#
#    def test_get_no_appeals_status(self):
#        response = self.client.get('/appeals')
#
#        self.assertEquals(response.status_code, 200)
#
#    def test_get_one_appeal_json(self):
#        appeal = self.post_test_appeal('gmail.com')
#
#        response = self.client.get('/appeals')
#
#        self.assertEquals(response.json,
#                          {'appeals': [appeal.json()]})
#
#    def test_get_one_appeal_status(self):
#        self.post_test_appeal('gmail.com')
#
#        response = self.client.get('/appeals')
#        self.assertEquals(response.status_code, 200)
#
#    def test_get_many_appeals_json(self):
#        appeals = [self.post_test_appeal('bing.com'),
#                   self.post_test_appeal('gmail.com')]
#
#        response = self.client.get('/appeals')
#
#        self.assertEquals(response.json,
#                          {'appeals':
#                           [appeal.json() for appeal in appeals]})
#
#    def test_get_many_appeals_status(self):
#        self.post_test_appeal('bing.com')
#        self.post_test_appeal('gmail.com')
#
#        response = self.client.get('/appeals')
#
#        self.assertEquals(response.status_code, 200)
