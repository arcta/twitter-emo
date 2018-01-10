from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
sql = SQLAlchemy()


def get_span():
    if int(datetime.now().strftime('%d')) > 10:
        return datetime.now().strftime('%Y-%m')
    return (datetime.now() - timedelta(days = 30))\
                    .strftime('%Y-%m')

def interval(days):
    return text('NOW() - INTERVAL {} DAY'.format(days))

def current():
    return text('CURDATE()')
    
    

class EmoModel(sql.Model):
    __tablename__ = 'emoji'
    __table_args__ = { 'mysql_charset': 'utf8mb4' }

    """
mysql> describe emoji;
+-------------+-------------+------+-----+---------+-------+
| Field       | Type        | Null | Key | Default | Extra |
+-------------+-------------+------+-----+---------+-------+
| code        | varchar(48) | NO   | PRI |         |       |
| chars       | varchar(8)  | NO   |     |         |       |
| composite   | tinyint(1)  | NO   |     | 0       |       |
| description | varchar(53) | NO   |     |         |       |
+-------------+-------------+------+-----+---------+-------+
    """
    code        = sql.Column(sql.String,  primary_key=True)
    chars       = sql.Column(sql.String,  nullable=False, default='')
    composite   = sql.Column(sql.Integer, nullable=False, default=0)
    description = sql.Column(sql.String,  nullable=False, default='')

    def __repr__(self):
        return '<Emo [{}]>'.format(self.description)

    @classmethod
    def get_all(model):
        return model.query\
            .with_entities(model.code, model.description)\
            .filter(model.composite == 1)\
            .order_by(model.code.asc())\
            .all()


class EmoSentModel(sql.Model):
    __tablename__ = 'emo_sent'

    """
mysql> describe emo_sent;
+-----------+-------------+------+-----+---------+-------+
| Field     | Type        | Null | Key | Default | Extra |
+-----------+-------------+------+-----+---------+-------+
| code      | varchar(48) | NO   | PRI |         |       |
| span      | char(7)     | NO   | PRI | 0000-00 |       |
| positive  | int(11)     | NO   |     | 0       |       |
| negative  | int(11)     | NO   |     | 0       |       |
| total     | int(11)     | NO   |     | 0       |       |
| sentiment | float       | NO   |     | 0       |       |
+-----------+-------------+------+-----+---------+-------+
    """
    code        = sql.Column(sql.String,  primary_key=True)
    span        = sql.Column(sql.String,  primary_key=True)
    positive    = sql.Column(sql.Integer, nullable=False, default=0)
    negative    = sql.Column(sql.Integer, nullable=False, default=0)
    total       = sql.Column(sql.Integer, nullable=False, default=0)
    sentiment   = sql.Column(sql.Float,   nullable=False, default=0.0)

    def __repr__(self):
        return '<EmoSent {} {} {}>'.format(self.code, self.span, self.sentiment)

    @classmethod
    def get_all(model):
        return sql.session.query(model.code, model.total, model.sentiment, EmoModel.description)\
            .filter(model.span == get_span())\
            .filter(model.code == EmoModel.code)\
            .order_by(model.total.desc())\
            .order_by(model.sentiment.asc())\
            .all()

    @classmethod
    def get_negative(model, support):
        return sql.session.query(model.code, model.total, model.negative, model.sentiment, EmoModel.description)\
            .filter(model.span == get_span())\
            .filter(model.negative >= support)\
            .filter(model.code == EmoModel.code)\
            .order_by(model.sentiment.asc())\
            .all()

    @classmethod
    def get_positive(model, support):
        return sql.session.query(model.code, model.total, model.positive, model.sentiment, EmoModel.description)\
            .filter(model.span == get_span())\
            .filter(model.positive >= support)\
            .filter(model.code == EmoModel.code)\
            .order_by(model.sentiment.desc())\
            .all()


class EmoRatioModel(sql.Model):
    __tablename__ = 'emo_job_stats'

    """
mysql> describe emo_job_stats;
+----------+---------+------+-----+---------+-------+
| Field    | Type    | Null | Key | Default | Extra |
+----------+---------+------+-----+---------+-------+
| span     | char(7) | NO   | PRI | 0000-00 |       |
| positive | int(11) | NO   |     | 0       |       |
| negative | int(11) | NO   |     | 0       |       |
+----------+---------+------+-----+---------+-------+
    """
    span        = sql.Column(sql.String,  primary_key=True)
    positive    = sql.Column(sql.Integer, nullable=False, default=0)
    negative    = sql.Column(sql.Integer, nullable=False, default=0)

    @classmethod
    def get_current(model):
        return model.query\
            .filter(model.span == get_span())\
            .first()

    @classmethod
    def get_history(model):
        return model.query\
            .order_by(model.span.desc())\
            .all()            


class GeoModel(sql.Model):
    __tablename__ = 'iso_codes'

    """
mysql> describe iso_codes;
+---------+-------------+------+-----+---------+-------+
| Field   | Type        | Null | Key | Default | Extra |
+---------+-------------+------+-----+---------+-------+
| country | varchar(44) | NO   |     |         |       |
| alpha2  | char(2)     | NO   | PRI | ??      |       |
| alpha3  | char(3)     | NO   |     | ???     |       |
| geoid   | char(3)     | NO   |     | 000     |       |
| lon     | float       | YES  |     | NULL    |       |
| lat     | float       | YES  |     | NULL    |       |
| width   | float       | YES  |     | NULL    |       |
| height  | float       | YES  |     | NULL    |       |
+---------+-------------+------+-----+---------+-------+
    """
    country = sql.Column(sql.String)
    alpha2  = sql.Column(sql.String,  primary_key=True)
    alpha3  = sql.Column(sql.String)
    geoid   = sql.Column(sql.String)
    lon     = sql.Column(sql.Float)
    lat     = sql.Column(sql.Float)
    width   = sql.Column(sql.Float)
    height  = sql.Column(sql.Float)

    @classmethod
    def get_all(model):
        return model.query.all()


class GeoSentModel(sql.Model):
    __tablename__ = 'geo_sent'

    """
mysql> describe geo_sent;
+--------------+---------+------+-----+------------+-------+
| Field        | Type    | Null | Key | Default    | Extra |
+--------------+---------+------+-----+------------+-------+
| country_code | char(2) | NO   | PRI | ??         |       |
| span         | date    | NO   | PRI | 0000-00-00 |       |
| sentiment    | float   | NO   |     | 0          |       |
+--------------+---------+------+-----+------------+-------+
    """
    country_code = sql.Column(sql.String,  primary_key=True)
    span         = sql.Column(sql.Date,    primary_key=True)
    sentiment    = sql.Column(sql.Float,   nullable=False, default=0.0)

    def __repr__(self):
        return '<GeoSent {} {}>'.format(self.country_code, self.span)

    @classmethod
    def get_range(model, days):
        return sql.session.query(model.span, model.sentiment, GeoModel.country)\
            .filter(model.span >= interval(days + 1))\
            .filter(model.span < current())\
            .filter(model.country_code == GeoModel.alpha2)\
            .order_by(GeoModel.country.asc())\
            .order_by(model.span.asc())\
            .all()


class GeoStatsModel(sql.Model):
    __tablename__ = 'geo_job_stats'

    """
mysql> describe geo_job_stats;
+--------------+---------+------+-----+------------+-------+
| Field        | Type    | Null | Key | Default    | Extra |
+--------------+---------+------+-----+------------+-------+
| country_code | char(2) | NO   | PRI | ??         |       |
| span         | date    | NO   | PRI | 0000-00-00 |       |
| total        | int(11) | NO   |     | 0          |       |
+--------------+---------+------+-----+------------+-------+
    """
    country_code = sql.Column(sql.String,  primary_key=True)
    span         = sql.Column(sql.Date,    primary_key=True)
    total        = sql.Column(sql.Float,   nullable=False, default=0.0)

    def __repr__(self):
        return '<GeoSTats {} {}>'.format(self.country_code, self.span)

    @classmethod
    def get_range(model, days):
        return sql.session.query(GeoModel.country, model.span, model.total)\
            .filter(model.span >= interval(days + 1))\
            .filter(model.span < current())\
            .filter(model.country_code == GeoModel.alpha2)\
            .order_by(model.country_code.asc())\
            .order_by(model.span.asc())\
            .all()
            
            

class EmoStatsModel(sql.Model):
    __tablename__ = 'emo_stats'

    """
mysql> describe emo_stats;
+--------------+-------------+------+-----+------------+-------+
| Field        | Type        | Null | Key | Default    | Extra |
+--------------+-------------+------+-----+------------+-------+
| code         | varchar(48) | NO   | PRI |            |       |
| country_code | char(2)     | NO   | PRI | ??         |       |
| span         | date        | NO   | PRI | 0000-00-00 |       |
| total        | int(11)     | NO   |     | 0          |       |
+--------------+-------------+------+-----+------------+-------+
    """
    code         = sql.Column(sql.String,  primary_key=True)
    country_code = sql.Column(sql.String,  primary_key=True)
    span         = sql.Column(sql.Date,    primary_key=True)
    total        = sql.Column(sql.Float,   nullable=False, default=0.0)

    def __repr__(self):
        return '<EmoStats {}:{}:{}>'.format(self.code, self.country_code, self.span)

    @classmethod
    def get_range(model, days):
        return sql.session.query(EmoModel.description, model.code,
                                 GeoModel.country, model.country_code,
                                 model.span, model.total)\
            .filter(model.span >= interval(days + 1))\
            .filter(model.span < current())\
            .filter(model.country_code == GeoModel.alpha2)\
            .filter(model.code == EmoModel.code)\
            .order_by(model.country_code.asc())\
            .order_by(model.span.asc())\
            .all()
