import os

from flask import Flask
from flask_restplus import Resource, Api, fields, abort

from pmip.data import load_from_s3_and_unpickle, get_latest_s3_dateint, load_from_fs_and_unpickle

DATA_DIR = "data"
MODEL_FILENAME = "model.pkl"


def possible_types(value):
    if value not in ('class', 'probability'):
        raise ValueError('Unexpected value {0}'.format(value))
    return value


if os.getenv('ENVIRONMENT', '') == 'dev':
    latest_model_id = 'local'
    model = load_from_fs_and_unpickle(
        filename='model.pkl',
        subdirectory='data',
    )
elif os.getenv('ENVIRONMENT', '') in ['staging', 'prod']:
    latest_model_id = get_latest_s3_dateint(
        datadir='models',
        bucket=os.getenv('BUCKET')
    )
    model = load_from_s3_and_unpickle(
        filename='model.pkl',
        subdirectory=f'models/{os.getenv("ENVIRONMENT")}/{latest_model_id}',
        bucket=os.getenv('BUCKET')
    )

app = Flask(__name__)
api = Api(app)

app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

parser = api.parser()
parser.add_argument('type', type=possible_types, help='Prediction type', default='class')

request = api.model('Comment', {
    'comments': fields.List(
        fields.String(description="Comment", example="Check it out this free stuff"),
        example=[
            "Check it out this free stuff",
            "I take issue with your characterization"
        ]
    ),
})


@api.route('/healthcheck')
class HelloWorld(Resource):
    def get(self):
        return {'status': 'ok'}


@api.route('/predict')
@api.response(400, 'Bad Request')
@api.response(404, 'Not found')
class Predict(Resource):

    @api.doc(body=request, parser=parser)
    @api.expect(request)
    # @api.marshal_with(request, code=201)
    def post(self):
        args = parser.parse_args()
        request_data = api.payload

        if len(request_data['comments']) == 0:
            abort(
                400,
                "You must provide at least one comment in the list"
            )

        if not all([isinstance(s, str) for s in request_data['comments']]):
            abort(
                400,
                "The comments list can only contain strings"
            )

        if args['type'] is None or args['type'] == 'class':
            val = model.predict(request_data['comments'])
            result = [{'class': int(s)} for s in val]
        elif args['type'] == 'probability':
            val = model.predict_proba(request_data['comments'])
            result = [{'probability': list(s)} for s in val]
        else:
            abort(
                400,
                f"Don't recognize type {type}"
            )

        return {'result': result}, 200


@api.route('/model-info')
class ModelInfo(Resource):

    def get(self):
        result = {
            "model_id": latest_model_id,
            "ENVIRONMENT": os.getenv('ENVIRONMENT', '')
        }

        return {'result': result}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
