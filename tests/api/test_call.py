from tests.test_template import BaseCase

from application.models.call import CallModel
from application.models.donation import DonationModel
from application.models.operator import OperatorModel
from application.models.lead import LeadModel
from application.models.appeal import AppealModel


def create_call():
    appeal = AppealModel('title', 'url')
    appeal.save_to_db()

    lead = LeadModel('email', 'phone', 'name', 'surname', appeal.id)
    lead.save_to_db()

    operator = OperatorModel('testuser', 'name', 'surname', 'email')
    operator.save_to_db()

    call = CallModel('04-12-2020', '03::04:05', lead.id, operator.id)
    call.save_to_db()

    return call


class DonationGetCase(BaseCase):
    def test_get_call_with_non_existing_id_response(self):
        response = self.client.get('/calls/1')

        self.assertEqual(response.json['message'],
                         'There is no call with this id')

#     def test_get_call_with_non_existing_id_status(self):
#         response = self.client.get('/calls/1')
# 
#         self.assertEqual(response.status_code, 404)
# 
#     def test_get_call_with_existing_id_json(self):
#         call = create_call()
# 
#         response = self.client.get("/calls/{}".format(call.id))
#         self.assertEqual(response.json, call.json())
# 
#     def test_get_with_existing_id_status(self):
#         call = create_call()
# 
#         response = self.client.get("/calls/{}".format(call.id))
#         self.assertEqual(response.status_code, 200)
# 
# 
# class DonationDeleteCase(BaseCase):
#     def test_delete_post_with_non_existing_id_json(self):
#         response = self.client.delete('/calls/8')
# 
#         self.assertEqual(response.json,
#                          {'message': 'There is no call with this id'})
# 
#     def test_delete_post_with_non_existing_id_status(self):
#         response = self.client.delete('/calls/8')
# 
#         self.assertEqual(response.status_code, 404)
# 
#     def test_delete_post_with_existing_id_json(self):
#         call = create_call()
# 
#         response = self.client.delete("/calls/{}".format(call.id))
# 
#         self.assertEqual(response.json, {'message': 'Donation deleted'})
# 
#     def test_delete_post_with_existing_id_status(self):
#         call = create_call()
# 
#         response = self.client.delete("/calls/{}".format(call.id))
# 
#         self.assertEqual(response.status_code, 200)
# 
# 
# class AppealPutCase(BaseCase):
#     def test_put_with_no_existing_id_json(self):
#         data = {}
# 
#         response = self.client.put("calls/2", data=data)
#         self.assertEqual(response.json,
#                          {'message': 'There is no call with this id'})
# 
#     def test_put_with_no_existing_id_status(self):
#         data = {}
# 
#         response = self.client.put('/calls/2', data=data)
#         self.assertEqual(response.status_code, 404)
# 
#     def test_put_with_existing_id_json(self):
#         data = {'frequency': 'Monthly'}
# 
#         call = create_call()
# 
#         response = self.client.put("/calls/{}".format(call.id),
#                                    data=data)
#         self.assertEqual(response.json,
#                          {'id': call.id, 'frequency': 'Monthly',
#                           'amount': 30.00,
#                           'operator_id': call.operator.id,
#                           'lead_id': call.lead.id})
# 
#     def test_put_with_existing_id_status(self):
#         data = {'frequency': 'Monthly'}
# 
#         call = create_call()
# 
#         response = self.client.put("/calls/{}".format(call.id),
#                                    data=data)
#         self.assertEqual(response.status_code, 200)
