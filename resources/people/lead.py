from flask_restful import Resource, reqparse

from models.people.lead import LeadModel


class Lead(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str)
    parser.add_argument('phone',
                        type=str)
    parser.add_argument('name',
                        type=str)
    parser.add_argument('surname',
                        type=str)

    def get(self, id):
        lead = LeadModel.find_by_id(id)

        if lead:
            return lead.json()

        return {'message': 'There is no lead with this email'}

    def put(self, id):
        lead = LeadModel.find_by_id(id)

        if lead:
            data = self.parser.parse_args()

            for attribute, value in data.items():
                if value:
                    setattr(lead, attribute, value)

            try:
                lead.save_to_db()
            except Exception:
                return {'message': 'An error occured updating a lead'}, 500

            return lead.json()

        return {'message': 'There is no lead with this id'}

    def delete(self, id):
        lead = LeadModel.find_by_id(id)

        if lead:
            lead.delete_from_db()

        return {'message': 'Lead deleted'}


class LeadList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="Email is required")
    parser.add_argument('phone',
                        type=str,
                        required=True,
                        help="Phone is required")
    parser.add_argument('name',
                        type=str)
    parser.add_argument('surname',
                        type=str)

    def get(self):
        return {'leads': [lead.json() for lead in
                          LeadModel.query.all()]}

    def post(self):
        data = self.parser.parse_args()

        if LeadModel.find_by_email(data['email']):
            return {'message': 'There is already a lead with this email'}

        lead = LeadModel(**data)

        try:
            lead.save_to_db()
        except Exception:
            return {'message': 'An error occured inserting a lead'}, 500

        return lead.json()
