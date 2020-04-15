from flask_resftul import Resource, reqparse
from models.people.lead import LeadModel


class Lead(Resource):
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

    def get(self, email):
        lead = LeadModel.find_by_email(email)

        if lead:
            return lead.json()

        return {'message': 'There is no lead with this email'}

    def post(self):
        data = self.parser.parse_args()
        lead = LeadModel.find_by_email(data['email'])

        if lead:
            return {'message': 'There is already a lead with this email'}

        try:
            lead.save_to_db()
        except Exception:
            return {'message': 'An error occured during operator insertion'}, \
                    500

    def put(self):
        data = self.parser.parse_args()
        lead = LeadModel.find_by_email(data('email'))

        if lead:
            lead.email = data['email']
            lead.phone = data['phone']
            lead.name = data['name']
            lead.surname = data['surname']
        else:
            try:
                lead.save_to_db()
            except Exception:
                return {'message': 'An error occured during operator'
                        'insertion'}

        return lead.json()

    def delete(self):
        data = self.parser.parse_args()
        lead = LeadModel.find_by_email(data('email'))

        if lead:
            lead.delete_from_db()

        return {'message': 'Lead deleted'}


class LeadList(Resource):
    def get(self):
        return {'leads': [lead.json() for lead in
                          LeadModel.query.all()]}
