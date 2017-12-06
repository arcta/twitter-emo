'use strict';

/**********************************************************************
 * pubsub Twitter *
 **********************************************************************/
exports.sample = function(req, res, next) {
    let count = 10,
        query = req.params.keyword || 'AI';

    if (req.params && req.params.count)
        count = Math.max(1, Math.min(parseInt(req.params.count, 10), 100));

    const exec = require('child_process').exec,
          path = process.env.PROJECTS_HOME +'/twitter/python/sample.py';
    exec('python '+ path +' '+ query +' '+ count, function(err, stdout, stderr) {
        if (err) res.error(err);
        res.status(200);
        res.send(stdout);
    });
};

exports.stream = function(req, res, next) {
    let minutes = 1,
        query = req.params.keyword,
        geo = (query == 'geo' ? 1:-1);

    if (req.params && req.params.minutes)
        minutes = Math.max(1, Math.min(parseInt(req.params.minutes, 10), 10));

    if (geo) query = 'AI';

    const spawn = require('child_process').spawn,
          path = process.env.PROJECTS_HOME +'/twitter/python/app.py';

    spawn('python', [path, query, geo, 1000000, minutes],
                { stdio: 'ignore', detached: true }).unref();
    return true;
};

exports.IN = function(channel, count) {
    //console.log('Twitter joined '+ channel +' ('+ count +')');
};

exports.OUT = function() {
    //console.log('Twitter left ...');
};

exports.DATA = function(channel, message) {
    //console.log('Twitter got DATA: '+ message +' on '+ channel);
};

exports.ERROR = function(err) {
    //console.log('Twitter ERROR: '+ err);
};

