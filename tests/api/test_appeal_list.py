from application.models.appeal import AppealModel

from tests.test_template import BaseCase


class AppealListPostCase(BaseCase):
    def post_test_appeal(self):
        appeal = AppealModel('test', 'http://test.com')
        appeal.save_to_db()
        return appeal

    def test_post_appeal_with_required_fields_status(self):
        data = {'url': 'http://test.com'}
        response = self.client.post('/appeals', data=data)
        self.assertEqual(response.json['url'], 'http://test.com')
        self.assertEqual(response.status_code, 200)

    def test_post_appeal_with_required_fields_json(self):
        data = {'url': 'http://test.com'}
        response = self.client.post('/appeals', data=data)
        appeal = AppealModel.query.all()[0]
        _id = appeal.id
        self.assertEqual(response.json,
                         {'id': _id, 'title': None,
                          'url': 'http://test.com'})

    def test_post_appeal_with_no_required_fields_status(self):
        data = {'incorrect_field': 'sss'}
        response = self.client.post('/appeals', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_appeal_with_no_required_fields_json(self):
        data = {'incorrect_field': 'sss'}
        response = self.client.post('/appeals', data=data)
        self.assertEqual(response.json,
                         {'message': {'url': 'A URL is required'}})

    def test_post_appeal_existing_appeal_json(self):
        appeal = self.post_test_appeal()
        url = appeal.url
        data = {'url': url}
        response = self.client.post('/appeals', data=data)
        self.assertEqual(response.json,
                         {'message':
                          'There is already an appeal with this url'})

    def test_post_appeal_existing_appeal_status(self):
        appeal = self.post_test_appeal()
        url = appeal.url
        data = {'url': url}
        response = self.client.post('/appeals', data=data)
        self.assertEqual(response.status_code, 400)


class AppealListGetCase(BaseCase):
    def post_test_appeal(self, url):
        appeal = AppealModel('test', url)
        appeal.save_to_db()

        return appeal

    def test_get_no_appeals_json(self):
        response = self.client.get('/appeals')

        self.assertEqual(response.json, {'appeals': []})

    def test_get_no_appeals_status(self):
        response = self.client.get('/appeals')

        self.assertEqual(response.status_code, 200)

    def test_get_one_appeal_json(self):
        appeal = self.post_test_appeal('gmail.com')

        response = self.client.get('/appeals')

        self.assertEqual(response.json,
                         {'appeals': [appeal.json()]})

    def test_get_one_appeal_status(self):
        self.post_test_appeal('gmail.com')

        response = self.client.get('/appeals')
        self.assertEqual(response.status_code, 200)

    def test_get_many_appeals_json(self):
        appeals = [self.post_test_appeal('bing.com'),
                   self.post_test_appeal('gmail.com')]

        response = self.client.get('/appeals')

        self.assertEqual(response.json,
                         {'appeals':
                          [appeal.json() for appeal in appeals]})

    def test_get_many_appeals_status(self):
        self.post_test_appeal('bing.com')
        self.post_test_appeal('gmail.com')

        response = self.client.get('/appeals')

        self.assertEqual(response.status_code, 200)
