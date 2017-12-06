from flask_restful import Resource, reqparse
from models.elastic import StarModel


class StarElastic(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type = str,
        required = True,
        help = 'Name cannot be blank!'
    )

    def get(self, name):
        star = StarModel.find_star_by_name(name)
        if star is None:
            return { 'message':'not found' }, 404
        return star


class DistanceElastic(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('threshold',
        type = float
    )

    def get(self, threshold):
        if threshold is None:
            threshold = 1e6
        return StarModel.find_close_stars(threshold)

