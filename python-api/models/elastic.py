import os
from elasticsearch import Elasticsearch

data = Elasticsearch([os.environ['ES_URI']])


class StarModel:

    @staticmethod
    def find_star_by_name(name):
        stars = data.search(index = 'stars', body = {'query':{'match':{'Name':name }}})
        if stars is None: return
        star = stars['hits']['hits'][0]
        return { k: star['_source'][k] for k in star['_source'] }


    @staticmethod
    def find_close_stars(threshold):
        stars = data.search(index = 'stars',
                            body = {'query':{'range':{'Distance':{'lt':threshold }}},
                                    'sort':[{'Distance':{'order':'asc'}}]})
        return [{ k: star['_source'][k] for k in star['_source'] } for star in stars['hits']['hits']]
