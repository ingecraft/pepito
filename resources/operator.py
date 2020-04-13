from flask_resftul import Resource
from models.operator import OperatorModel


class Operator(Resource):
    def get(self, _id):
        operator = OperatorModel.get_by_id(_id)
        if operator:
            return operator.json()

        return {'message': "There is no operator with id:"
                "'{}'".format(self._id)}

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class OperatorList(Resource):
    def get(self):
        pass
