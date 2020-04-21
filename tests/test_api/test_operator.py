from tests.test_template import BaseCase


class OperatorPostMethodCase(BaseCase):
    def post_test_operator(self):
        data = {'username': 'Bob'}
        self.client.post('/operators', data=data)

    def test_post_with_required_fields_200_OK(self):
        data = {'username': 'Bob'}
        response = self.client.post('/operators', data=data)
        self.assertEquals(response.json['username'], 'Bob')
        self.assertEquals(response.status_code, 200)

    def test_post_with_no_required_fields_400_Bad_request(self):
        data = {'incorrect_field': 'Bob'}
        response = self.client.post('/operators', data=data)
        self.assertEquals(response.status_code, 400)

    def test_post_existing_operator(self):
        self.post_test_operator()
        data = {'username': 'Bob'}
        response = self.client.post('/operators', data=data)
        self.assertEquals(response.json['message'], 'Username already exists')
