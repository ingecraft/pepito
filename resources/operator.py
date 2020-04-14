from flask_restful import Resource, reqparse
from models.operator import OperatorModel


class Operator(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="Email is required")
    parser.add_argument('name',
                        type=str)
    parser.add_argument('surname',
                        type=str)

    def get(self, username):
        operator = OperatorModel.find_by_username(username)

        if operator:
            return operator.json()

        return {'message': "Username does not exist"}

    def post(self, username):
        if OperatorModel.find_by_username(username):
            return {'message': 'Username already exists'}

        data = self.parser.parse_args()
        operator = OperatorModel(username, **data)

        try:
            operator.save_to_db()
        except Exception:
            return {'message': 'An error occured during operator insertion'}, \
                    500

        return operator.json()

    def put(self, username):
        operator = OperatorModel.find_by_username(username)

        data = self.parser.parse_args()

        if operator:
            operator.email = data['email']
            operator.name = data['name']
            operator.surname = data['surname']
        else:
            operator = OperatorModel(username, **data)

        operator.save_to_db()

        return operator.json()

    def delete(self, username):
        operator = OperatorModel.find_by_username(username)

        if operator:
            operator.delete_from_db()

        return {'message': 'Operator deleted'}


class OperatorList(Resource):
    def get(self):
        return {'operators': [operator.json() for operator in
                              OperatorModel.query.all()]}
