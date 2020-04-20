from flask_restful import Resource, reqparse

from application.models.call import CallModel


class Call(Resource):
    def get(self, id):
        call = CallModel.find_by_id(id)

        if call:
            return call.json()

        return {'message': 'There is no call with this id'}

    def delete(self, id):
        call = CallModel.find_by_id(id)

        if call:
            call.delete_from_db()

        return {'message': 'Call deleted'}


class CallList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date',
                        type=str)
    parser.add_argument('time',
                        type=str)
    parser.add_argument('duration',
                        type=float)
    parser.add_argument('operator_id',
                        type=str,
                        required=True,
                        help='Operator id is required')
    parser.add_argument('lead_id',
                        type=str,
                        required=True,
                        help='Lead id is required')

    def get(self):
        return {'calls': [call.json() for call in
                          CallModel.query.all()]}

    def post(self):
        data = self.parser.parse_args()

        call = CallModel(**data)

        try:
            call.save_to_db()
        except Exception:
            return {'message': 'An error occured inserting a call'}, 500

        return call.json()
