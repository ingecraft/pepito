from tests.test_template import BaseCase
from application.models.operator import OperatorModel


class OperatorGetCase(BaseCase):
    def create_operator(self):
        operator = OperatorModel('bobcat', 'Bob', 'Cat', 'bob@cat.com')
        operator.save_to_db()
        return operator

    def test_get_operator_with_non_existing_id_response(self):
        response = self.client.get('/operators/1')
        self.assertEquals(response.json['message'],
                          'There is no operator with given id')

    def test_get_operator_with_non_existing_id_status(self):
        response = self.client.get('/operators/1')
        self.assertEquals(response.status_code, 404)

    def test_get_operator_with_existing_id_json(self):
        operator = self.create_operator()
        _id = operator.json()['id']
        response = self.client.get("/operators/{}".format(_id))
        self.assertEquals(response.json, operator.json())

    def test_get_operator_with_existing_id_status(self):
        operator = self.create_operator()
        _id = operator.json()['id']
        response = self.client.get("/operators/{}".format(_id))
        self.assertEquals(response.status_code, 200)


class OperatorDeleteCase(BaseCase):
    def create_operator(self):
        operator = OperatorModel('bobcat', 'Bob', 'Cat', 'bob@cat.com')
        operator.save_to_db()
        return operator

    def test_delete_operator_with_non_existing_id_json(self):
        response = self.client.delete('/operators/8')
        self.assertEquals(response.json,
                          {'message': 'There is no operator with this id'})

    def test_delete_operator_with_non_existing_id_status(self):
        response = self.client.delete('/operators/8')
        self.assertEquals(response.status_code, 404)

    def test_delete_operator_with_existing_id_json(self):
        operator = self.create_operator()
        _id = operator.json()['id']
        response = self.client.delete("/operators/{}".format(_id))
        self.assertEquals(response.json, {'message': 'Operator deleted'})

    def test_delete_operator_with_existing_id_status(self):
        print(len(OperatorModel.query.all()))
        operator = self.create_operator()
        print(len(OperatorModel.query.all()))
        _id = operator.json()['id']
        response = self.client.delete("/operators/{}".format(_id))
        self.assertEquals(response.status_code, 200)
