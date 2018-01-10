'use strict';

/**********************************************************************
 * basic MongoDB client *
 **********************************************************************/
var Mongo = require('mongodb').MongoClient,

    opt = {
            server: {
                auto_reconnect: true,
                poolSize: 100,
                socketOptions: {
                    connectTimeoutMS: 5000,
                }
            }
        },

    mongodb,
    url;


exports.connect = function(conf, options, callback) {
    options = options || opt;
    callback = callback || function(){},
    url = conf.getConf('MONGO_URI');
    //url = process.env.MONGO_URI;

    Mongo.connect(url, opt, function(err, db) {
        if (err) return console.log(err);
        mongodb = db
        callback();
        return !!db;
    });
};


exports.db = function() {
    return mongodb;
};
