from datetime import datetime

from flask_restful import Resource, reqparse

from models.assets.donation import DonationModel


class Donation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str)
    parser.add_argument('url',
                        type=str)

    def get(self, id):
        donation = DonationModel.find_by_id(id)

        if donation:
            return donation.json()

        return {'message': 'There is no donation with this id'}

    def put(self, id):
        pass
#        appeal = AppealModel.find_by_id(id)
#
#        if appeal:
#            data = self.parser.parse_args()
#
#            for attribute, value in data.items():
#                if value:
#                    setattr(appeal, attribute, value)
#
#            try:
#                appeal.save_to_db()
#                return appeal.json()
#            except Exception:
#                return {'message': 'An error occured updating'
#                        'an appeal.'}, 500
#
#        return {'message': 'There is no appeal with this id'}
#

    def delete(self, id):
        pass
#        appeal = AppealModel.find_by_id(id)
#
#        try:
#            appeal.delete_from_db()
#        except Exception:
#            return {'message': 'Error deleting the appeal'}, 500
#
#        return {'message': 'Appeal deleted'}


class DonationList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('frequency',
                        type=str,
                        required=True,
                        help='Frequency is required')
    parser.add_argument('amount',
                        type=float,
                        required=True,
                        help='Amount is required')
    parser.add_argument('operator_id',
                        type=int,
                        required=True,
                        help='An operator is required')
    parser.add_argument('lead_id',
                        type=int,
                        required=True,
                        help='A lead is required')

    def get(self):
        pass
        return {'appeals': [appeal.json() for appeal in
                            DonationModel.query.all()]}

    def post(self):
        data = self.parser.parse_args()

        if DonationModel.find_by_lead_id(data['lead_id']):
            return {'message': 'There is already a donation for this lead'}

        donation = DonationModel(**data)

        try:
            donation.save_to_db()
        except Exception:
            return {'message': 'An error occured inserting the donation'}, 500

        return donation.json()
