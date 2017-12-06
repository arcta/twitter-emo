from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import desc
from collections import namedtuple


sc = SparkContext()

ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)
ssc.checkpoint('/tmp/checkpoint')

# python stream-socket.py QUERY PORT
port = 9999
stream = ssc.socketTextStream(os.environ['NODEIP'], port)

lines = stream.window(10)
fields = ('tag', 'count')
Tweet = namedtuple('Tweet', fields)

#msg = json.loads(data)
#self.broadcast(msg['text'].encode('utf-8'))

(lines.flatMap( lambda text: text.split(' '))
    .filter( lambda word: word.lower().startswith('#'))
    .map( lambda word: ( word.lower(), 1 ))
    .reduceByKey( lambda a, b: a + b )
    .map( lambda rec: Tweet( rec[0], rec[1] ))
    .foreachRDD( lambda rdd: rdd.toDF().sort( desc('count'))
              .limit(10).registerTempTable('tweets')))

if  __name__ =='__main__':
    ssc.start()
