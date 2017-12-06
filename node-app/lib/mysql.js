'use strict';

/**********************************************************************
 * basic MySQL client *
 **********************************************************************/
var MySQL = require('mysql'),
    pool = null;


exports.connect = function(config) {
    pool = MySQL.createPool({
        host : config.getConf('MYSQL_HOST'),
        port : config.getConf('MYSQL_PORT'),
        user : config.getConf('DATAUSER'),
        password: config.getConf('MYSQL_PASS'),
        database: config.getConf('DATABASE')
    });
    return !!pool;
};


exports.pool = function() {
    return pool;
};
