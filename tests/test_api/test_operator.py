from tests.test_template import BaseCase


class OperatorPostMethodCase(BaseCase):
    def test_post_with_required_fields_200_OK(self):
        data = {'username': 'Bob'}
        request = self.client.post('/operators', data=data)
        self.assertEquals(request.json['username'], 'Bob')
