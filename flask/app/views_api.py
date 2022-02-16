# https://flask-restx.readthedocs.io/en/latest/quickstart.html
from app import api
from app.views import query_db, query_all, total
from flask_restx import Resource, fields, reqparse
from werkzeug.exceptions import BadRequest

parser = reqparse.RequestParser()
parser.add_argument('limit', required=True, type=int)
parser.add_argument('offset', required=True, type=int)

model_apinat = api.model('nat', {
    'address': fields.String,
    'count': fields.Integer,
    'results': fields.List(fields.Raw)
})

model_apinatall = api.model('nats', {
    'offset': fields.Integer(min=0),
    'limit': fields.Integer(max=1000),
    'total': fields.Integer,
    'results': fields.List(fields.Raw)
})


@api.route("/nat/<string:address>")
@api.doc(params={'address': 'IPv4 Address'})
class apinat(Resource):
    @api.marshal_with(model_apinat)
    def get(self, address):
        if address.count(".") == 3:
            rules = query_db(address)
            resp_data = {}
            resp_data["address"] = address
            resp_data["count"] = len(rules)
            resp_data["results"] = rules
            return resp_data
        else:
            raise BadRequest('Invalid address')

@api.route("/nats/")
@api.doc(params={
    'offset': 'Skip that many results before beginning to return them.',
    'limit': 'No more than that many results will be returned.'
})
class apinatall(Resource):
    @api.expect(parser)
    @api.marshal_with(model_apinatall)
    def get(self):
        args = parser.parse_args(strict=True)
        if (args.get("limit") > 0 and args.get("limit")<=2000) and (args.get("offset")>=0 and args.get("offset")<total):
            resp_data = query_all(offset=args.get("offset"), limit=args.get("limit"))
            return resp_data
        else:
            raise BadRequest('Invalid offset or limit value')
