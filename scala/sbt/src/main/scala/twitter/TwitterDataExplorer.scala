package me.arcta.twitter

import org.apache.spark._
import org.apache.spark.SparkContext._
import org.apache.spark.streaming._
import org.apache.spark.streaming.twitter._
import org.apache.spark.streaming.StreamingContext._
import org.apache.log4j.Level

import java.util.regex.Pattern
import java.util.regex.Matcher
import scala.util.Properties

import java.util.concurrent._
import java.util.concurrent.atomic._


/** Simple application to listen to a stream of Tweets */
object TwitterDataExplorer {
    /** Log error messages only */
    def setupLogging() = {
        import org.apache.log4j.{ Level, Logger }
        val rootLogger = Logger.getRootLogger()
        rootLogger.setLevel(Level.ERROR)
    }

    /** Configures Twitter API credentials using environment variables */
    def setupTwitter() = {
        val props = List("consumer_Key", "consumer_Secret", "access_Token", "access_Token_Secret")
        for (prop <- props) {
            val local = "TWITTER_" + prop.toUpperCase
            val conf = Properties.envOrElse(local, "")
            if (conf != "") {
                val name = prop.filterNot( _ == '_' )
                System.setProperty("twitter4j.oauth." + name, conf)
                println("Set Twitter auth." + name)
            } else {
                println("Missing Twitter credentials (env): " + local)
            }
        }
    }

    /** Our main function where the action happens */
    def main(args: Array[String]) {

        setupLogging()
        setupTwitter()

        // Set up a Spark streaming context named "PrintTweets" 1sec batches of data
        val conf = new SparkConf().setAppName("TwitterDataExplorer")
        val ssc = new StreamingContext(conf, Seconds(1))

        // Create a DStream from Twitter using our streaming context
        val tweets = TwitterUtils.createStream(ssc, None)
        // Extract the text of each status update into RDD's
        val statuses = tweets.map(status => status.getText())

        // Print out the first ten
        //statuses.print()

        // Keep count of how many Tweets we've received
        var total: Long = 0

        statuses.foreachRDD((rdd, time) => {
            // Don't bother with empty batches
            if (rdd.count() > 0) {
                // Combine each partition's results into a single RDD:
                val repartitionedRDD = rdd.repartition(1).cache()
                repartitionedRDD.saveAsTextFile("tweets-" + time.milliseconds.toString)
                // Stop once we've collected 1000 tweets.
                total += repartitionedRDD.count()
                println("Tweet count: " + total)
                if (total > 1000) {
                    System.exit(0)
                }
            }
        })

        // Map to tweet character lengths
        val lengths = statuses.map(status => status.length())

        // As we could have multiple processes adding into these running totals
        // Java's AtomicLong class to make sure these counters are thread-safe
        var totalTweets = new AtomicLong(0)
        var totalChars = new AtomicLong(0)

        lengths.foreachRDD((rdd, time) => {
            val count = rdd.count()
            if (count > 0) {
                totalTweets.getAndAdd(count)
                totalChars.getAndAdd(rdd.reduce((x,y) => x + y))
                println("Average length: " + totalChars.get() / totalTweets.get())
            }
        })

        // Blow out each word into a new DStream
        val words = statuses.flatMap(tweetText => tweetText.split(" "))
        // Now eliminate anything that's not a hashtag
        val hashtags = words.filter(word => word.startsWith("#"))
        // Map each hashtag to a key/value pair of (hashtag, 1)
        val hashtagKeyValues = hashtags.map(hashtag => (hashtag, 1))
        // Now count them up over a 5 minute window sliding every 1 second
        val hashtagCounts = hashtagKeyValues.reduceByKeyAndWindow(_ + _, _ - _, Seconds(300), Seconds(1))
        // Sort the results by the count values
        val result = hashtagCounts.transform(rdd => rdd.sortBy(x => x._2, false))
        // Print the top 10
        result.print

        // Set a checkpoint directory, and kick it all off
        ssc.checkpoint("/tmp/checkpoint/")
        ssc.start()
        ssc.awaitTermination()
    }
}
