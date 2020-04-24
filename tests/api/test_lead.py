from tests.test_template import BaseCase
from application.models.appeal import AppealModel


class AppealGetCase(BaseCase):
    def create_appeal(self):
        appeal = AppealModel('Test title', 'test.url')
        appeal.save_to_db()
        return appeal

    def test_get_with_non_existing_id_response(self):
        response = self.client.get('/appeals/1')
        self.assertEqual(response.json['message'],
                         'There is no appeal with this id')

    def test_get_with_non_existing_id_status(self):
        response = self.client.get('/appeals/1')
        self.assertEqual(response.status_code, 404)

    def test_get_with_existing_id_json(self):
        appeal = self.create_appeal()
        _id = appeal.json()['id']
        response = self.client.get("/appeals/{}".format(_id))
        self.assertEqual(response.json, appeal.json())

    def test_get_with_existing_id_status(self):
        appeal = self.create_appeal()
        _id = appeal.json()['id']
        response = self.client.get("/appeals/{}".format(_id))
        self.assertEqual(response.status_code, 200)


class AppealDeleteCase(BaseCase):
    def create_appeal(self):
        appeal = AppealModel('Test title', 'test.url')
        appeal.save_to_db()
        return appeal

    def test_delete_post_with_non_existing_id_json(self):
        response = self.client.delete('/appeals/8')
        self.assertEqual(response.json,
                         {'message': 'There is no appeal with this id'})

    def test_delete_post_with_non_existing_id_status(self):
        response = self.client.delete('/appeals/8')
        self.assertEqual(response.status_code, 404)

    def test_delete_post_with_existing_id_json(self):
        appeal = self.create_appeal()
        _id = appeal.json()['id']
        response = self.client.delete("/appeals/{}".format(_id))
        self.assertEqual(response.json, {'message': 'Appeal deleted'})

    def test_delete_post_with_existing_id_status(self):
        appeal = self.create_appeal()
        _id = appeal.json()['id']
        response = self.client.delete("/appeals/{}".format(_id))
        self.assertEqual(response.status_code, 200)


class AppealPutCase(BaseCase):
    def create_appeal(self):
        appeal = AppealModel('Test title', 'test.url')
        appeal.save_to_db()

        return appeal

    def test_put_with_no_existing_id_json(self):
        data = {}

        response = self.client.put("appeals/2", data=data)
        self.assertEqual(response.json,
                         {'message': 'There is no appeal with this id'})

    def test_put_with_no_existing_id_status(self):
        data = {}

        response = self.client.put('/appeals/2', data=data)
        self.assertEqual(response.status_code, 404)

    def test_put_with_existing_id_json(self):
        data = {'url': 'updated'}

        appeal = self.create_appeal()
        _id = appeal.json()['id']

        response = self.client.put("/appeals/{}".format(_id),
                                   data=data)
        self.assertEqual(response.json,
                         {'id': _id, 'url': 'updated', 'title': 'Test title'})

    def test_put_with_existing_id_status(self):
        data = {'url': 'updated'}

        appeal = self.create_appeal()
        _id = appeal.json()['id']

        response = self.client.put("/appeals/{}".format(_id),
                                   data=data)
        self.assertEqual(response.status_code, 200)
