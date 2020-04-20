from test_template import TestTemplate


class OperatorTestCase(TestTemplate):
    def test_post_new_operator_with_all_required_fields_200_OK(self):
        data = {'username': 'bob'}
        response = self.client.post('/operators', data=data)
        json_response = response.json
        assert json_response['username'] == 'bob'

    def test_get_operators_200_OK(self):
        response = self.client.get('/operators')
        assert response.status_code == 200
