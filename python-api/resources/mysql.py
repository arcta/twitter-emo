from flask import jsonify
from flask_restful import Resource, reqparse
from models.mysql import *


class Emo(Resource):
    def get(self):
        data = EmoModel.get_all()
        if data is None:
            return { 'message':'no data ...' }, 404
        return { d._asdict()['code']:d._asdict()['description']
                    for d in data }


class EmoSent(Resource):
    def get(self):
        data = EmoSentModel.get_all()
        return [ d._asdict() for d in data ]


class EmoPositive(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('support',
        type = int,
        required = True,
        help = 'Support sould be positive non-zero integer'
    )
    def get(self, support):
        data = EmoSentModel.get_positive(support)
        return [ d._asdict() for d in data ]


class EmoNegative(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('support',
        type = int,
        required = True,
        help = 'Support sould be positive non-zero integer'
    )
    def get(self, support):
        data = EmoSentModel.get_negative(support)
        return [ d._asdict() for d in data ]

    
class EmoRatioCurrent(Resource):
    def get(self):
        data = EmoRatioModel.get_current()
        if data.positive == 0:
            return 'N/A'
        return data.negative/data.positive


class EmoRatioHistory(Resource):
    def get(self):
        data = EmoRatioModel.get_history()
        return [ (d.span, d.negative/d.positive) for d in data ]


class GeoSentCurrent(Resource):
    def get(self):
        data = GeoSentModel.get_range(1)
        return [ (d.country, float(d.sentiment)) for d in data ]


class GeoSentHistory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('days',
        type = int,
        required = True,
        help = 'Days sould be positive non-zero integer'
    )
    def get(self, days):
        data = GeoSentModel.get_range(days)
        return [ (d.country, float(d.sentiment), str(d.span)) for d in data ]


class EmoStatsCurrent(Resource):
    def get(self):
        data = EmoStatsModel.get_range(1)
        norm = 0.01 * sum([int(d.total) for d in data])
        return [ (d.description, d.country, int(d.total)/norm) for d in data ]


class EmoStatsHistory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('days',
        type = int,
        required = True,
        help = 'Days sould be positive non-zero integer'
    )
    def get(self, days):
        data = EmoStatsModel.get_range(days)
        norm = {}
        for d in data:
            norm[str(d.span)] = norm.get(str(d.span), 0) + int(d.total)
        return [ (d.description,
                  d.country, 100.0 * int(d.total)/norm[str(d.span)],
                  str(d.span)) for d in data ]
    

class GeoStatsCurrent(Resource):
    def get(self):
        data = GeoStatsModel.get_range(1)
        norm = 0.01 * sum([int(d.total) for d in data])
        return [ (d.country, int(d.total)/norm) for d in data ]


class GeoStatsHistory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('days',
        type = int,
        required = True,
        help = 'Days sould be positive non-zero integer'
    )
    def get(self, days):
        data = GeoStatsModel.get_range(days)
        norm = {}
        for d in data:
            norm[str(d.span)] = norm.get(str(d.span), 0) + int(d.total)
        return [ (d.country,
                  100.0 * int(d.total)/norm[str(d.span)],
                  str(d.span)) for d in data ]
    