import os

from flask import Flask, render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from resources.mysql import *


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['MYSQL_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600


api = Api(app)
sql = SQLAlchemy(app)
sql.init_app(app)

class HelloAPI(Resource):
    def get(self):
        return { 'API end-points':{
            '/emo':'get all (non-composite) emojis',
            '/emo/score':'get all with scores',
            '/emo/positive/<int:support>':'get all with positive minimal support',
            '/emo/negative/<int:support>':'get all with negative minimal support',
            '/emo/ratio/history':'get history for negative over positive ratio',
            '/emo/ratio/current':'get current negative over positive ratio',
            '/geo/sent/current':'get current geo sentiment stats',
            '/geo/sent/history/<int:days>':'get geo sentiment stats for recent days',
            '/emo/rate/current':'get current emoji by country rate',
            '/emo/rate/history/<int:days>':'get emoji by country rate recent days',
            '/geo/rate/current':'get current country counts',
            '/geo/rate/history/<int:days>':'get country counts for recent days'
        }}

api.add_resource(HelloAPI,        '/')
api.add_resource(Emo,             '/emo')
api.add_resource(EmoSent,         '/emo/score')
api.add_resource(EmoPositive,     '/emo/positive/<int:support>')
api.add_resource(EmoNegative,     '/emo/negative/<int:support>')
api.add_resource(EmoRatioCurrent, '/emo/ratio/current')
api.add_resource(EmoRatioHistory, '/emo/ratio/history')
api.add_resource(GeoSentCurrent,  '/geo/sent/current')
api.add_resource(GeoSentHistory,  '/geo/sent/history/<int:days>')
api.add_resource(EmoStatsCurrent, '/emo/rate/current')
api.add_resource(EmoStatsHistory, '/emo/rate/history/<int:days>')
api.add_resource(GeoStatsCurrent, '/geo/rate/current')
api.add_resource(GeoStatsHistory, '/geo/rate/history/<int:days>')


@app.route('/geo')
def about():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True)
