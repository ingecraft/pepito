from flask_restful import Resource, reqparse

from application.models.operator import OperatorModel


class Operator(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str)
    parser.add_argument('email',
                        type=str)
    parser.add_argument('name',
                        type=str)
    parser.add_argument('surname',
                        type=str)

    def get(self, id):
        operator = OperatorModel.find_by_id(id)

        if operator:
            return operator.json()

        return {'message': "There is no operator with given id"}, 404

    def put(self, id):
        operator = OperatorModel.find_by_id(id)

        if operator:
            data = self.parser.parse_args()

            for attribute, value in data.items():
                if value:
                    setattr(operator, attribute, value)

            try:
                operator.save_to_db()
            except Exception:
                return {'message': 'An error occured inserting an operator'}, \
                        500

            return operator.json()

        return {'message': 'There is no operator with this id'}

    def delete(self, id):
        operator = OperatorModel.find_by_id(id)

        if operator:
            operator.delete_from_db()
            return {'message': 'Operator deleted'}

        return {'message': 'There is no operator with this id'}, 404


class OperatorList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username is required")
    parser.add_argument('email',
                        type=str)
    parser.add_argument('name',
                        type=str)
    parser.add_argument('surname',
                        type=str)

    def get(self):
        return {'operators': [operator.json() for operator in
                              OperatorModel.query.all()]}

    def post(self):
        data = self.parser.parse_args()

        if OperatorModel.find_by_username(data['username']):
            return {'message': 'Username already exists'}

        operator = OperatorModel(**data)

        try:
            operator.save_to_db()
        except Exception:
            return {'message': 'An error occured inserting an operator'}, 500

        return operator.json()
