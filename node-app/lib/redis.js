'use strict';

/**********************************************************************
 * basic Redis client *
 **********************************************************************/
var config = require('./config'),
    redis = require('redis').createClient;

exports.client = function() {
    var opt = config.getConf('REDIS_PASS') ?
        { auth_pass: config.getConf('REDIS_PASS') } : {};

    return redis(
            config.getConf('REDIS_PORT') || 6379,
            config.getConf('REDIS_HOST') || '127.0.0.1',
            opt);
};
