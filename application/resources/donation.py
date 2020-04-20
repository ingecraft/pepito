from flask_restful import Resource, reqparse

from application.models.donation import DonationModel


class Donation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('frequency',
                        type=str)
    parser.add_argument('amount',
                        type=float)
    parser.add_argument('lead_id',
                        type=int)
    parser.add_argument('operator_id',
                        type=int)

    def get(self, id):
        donation = DonationModel.find_by_id(id)

        if donation:
            return donation.json()

        return {'message': 'There is no donation with this id'}

    def put(self, id):
        donation = DonationModel.find_by_id(id)

        if donation:
            data = self.parser.parse_args()

            for attribute, value in data.items():
                if value:
                    setattr(donation, attribute, value)

            try:
                donation.save_to_db()
                return donation.json()
            except Exception:
                return {'message': 'An error occured updating'
                        'an donation.'}, 500

        return {'message': 'There is no donation with this id'}

    def delete(self, id):
        pass
        donation = DonationModel.find_by_id(id)

        try:
            donation.delete_from_db()
        except Exception:
            return {'message': 'Error deleting the donation'}, 500

        return {'message': 'Donation deleted'}


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
        return {'donations': [donation.json() for donation in
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
