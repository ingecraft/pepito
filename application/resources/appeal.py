from flask_restful import Resource, reqparse

from application.models.appeal import AppealModel


class Appeal(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str)
    parser.add_argument('url',
                        type=str)

    def get(self, id):
        appeal = AppealModel.find_by_id(id)

        if appeal:
            return appeal.json()

        return {'message': 'There is no appeal with this id'}

    def put(self, id):
        appeal = AppealModel.find_by_id(id)

        if appeal:
            data = self.parser.parse_args()

            for attribute, value in data.items():
                if value:
                    setattr(appeal, attribute, value)

            try:
                appeal.save_to_db()
                return appeal.json()
            except Exception:
                return {'message': 'An error occured updating'
                        'an appeal.'}, 500

        return {'message': 'There is no appeal with this id'}

    def delete(self, id):
        appeal = AppealModel.find_by_id(id)

        try:
            appeal.delete_from_db()
        except Exception:
            return {'message': 'Error deleting the appeal'}, 500

        return {'message': 'Appeal deleted'}


class AppealList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str)
    parser.add_argument('url',
                        type=str,
                        required=True,
                        help='A URL is required')

    def get(self):
        return {'appeals': [appeal.json() for appeal in
                            AppealModel.query.all()]}

    def post(self):
        data = self.parser.parse_args()

        if AppealModel.find_by_url(data['url']):
            return {'message': 'There is already a lead with this url'}

        appeal = AppealModel(**data)

        try:
            appeal.save_to_db()
        except Exception:
            return {'message': 'An error occured inserting an appeal'}, 500

        return appeal.json()
