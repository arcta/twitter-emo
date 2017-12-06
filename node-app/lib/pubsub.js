'use strict';

/**********************************************************************
 * basic PubSub with Redis *
 **********************************************************************/
const config = require('../lib/config'),
      logger = require('../lib/log'),
      pub = require('../lib/redis').client(),
      sub = require('../lib/redis').client();


exports.run = function(io, handler) {
    handler = handler || {};
    handler.IN  = handler.IN  || function(channel, count){};
    handler.OUT = handler.OUT || function(){};
    handler.DATA  = handler.DATA || function(channel, message){};
    handler.ERROR = handler.ERROR || function(err){};

    sub.on('subscribe', function(channel, count) {
        logger.app.info('SUB: '+ channel);
        handler.IN(channel, count)
    });

    sub.on('error', function(err) {
        logger.app.error('SUB: '+ err);
        handler.ERROR(err);
    });

    sub.subscribe('twitter-app')
    sub.subscribe('twitter-lang')
    sub.subscribe('twitter-words')
    sub.subscribe('twitter-emojis')
    sub.subscribe('twitter-hashtags')
    sub.subscribe('twitter-sentiment')
    sub.subscribe('twitter-country')
    sub.subscribe('twitter-place')
    sub.subscribe('twitter-box')

    io.sockets.on('connection', function(socket) {

        function follow(channel, message) {
            socket.emit(channel, message);
            //logger.app.info('FOLLOW: '+ channel);
            handler.DATA(channel, message);
        }

        sub.on('message', follow);

        socket.on('disconnect', function() {
            sub.removeListener('message', follow);
            handler.OUT();
        });
    });
};

exports.subscribe = function(channel) {
    sub.subscribe(channel);
};

exports.publish = function(channel, data) {
    pub.publish(channel, JSON.stringify(data));
};
