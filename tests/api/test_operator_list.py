from tests.test_template import BaseCase


class OperatorListPostCase(BaseCase):
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


class OperatorListGetCase(BaseCase):
    def post_test_operator(self, name):
        data = {'username': name}
        self.client.post('/operators', data=data)

    def test_get_no_operators(self):
        response = self.client.get('/operators')
        self.assertEquals(response.json, {'operators': []})

    def test_get_one_operator(self):
        self.post_test_operator('Bob')
        response = self.client.get('/operators')
        self.assertEquals(len(response.json['operators']), 1)

    def test_get_many_operators(self):
        self.post_test_operator('Bob')
        self.post_test_operator('Bill')
        response = self.client.get('/operators')
        self.assertEquals(len(response.json['operators']), 2)

