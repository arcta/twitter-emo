'use strict';

/**********************************************************************
 * DEPENDENCIES *
 **********************************************************************/
const express = require('express'),
      http = require('http'),
      path = require('path'),
      app = express(),

      config = require('./lib/config'),
      logger = require('./lib/log'),

      hbs = require('express-handlebars'),
      bundler = require('./lib/bundle'),
      pubsub = require('./lib/pubsub'),

      statics = require('serve-static'),
      favicon = require('serve-favicon'),
      compress = require('compression'),
      cors = require('cors'),

      project = __dirname.split('/')[4],
      port = config.getPort(project),

      server = http.createServer(app),
      io = require('socket.io')(server);

app.use(statics(path.join(__dirname, 'static')));
app.use(favicon(path.join(__dirname, 'static/favicon.png')));
app.use(compress());
app.use(cors({ origin:config.getConf('ALLOW_ORIGIN') || '*' }));

app.engine('.hbs', hbs({ extname: '.hbs' }));
app.set('view engine', '.hbs');

logger.log(__dirname, 'ALL');

/**********************************************************************
 * MODELS *
 **********************************************************************/
const Twitter = require('./twitter');
pubsub.run(io, Twitter);

/**********************************************************************
 * ROUTES *
 **********************************************************************/
app.get('/', function(req, res, next) {
    res.sendFile(__dirname + '/static/index.html');
});

app.get('/', function(req, res, next) {
    res.sendFile(__dirname + '/static/index.html');
});

app.get('/sample', Twitter.sample);
app.get('/sample/:keyword/:count', Twitter.sample);

app.get('/stream/:keyword/:minutes', function(req, res, next) {
    if (req.params.keyword == 'geo' && Twitter.stream(req, res, next))
        bundler.render(res, 'viz', 'geo', ['viz-geo'], 'Geo');
    else res.send(req.params.keyword);
});

app.get('/VR/:minutes', function(req, res, next) {
    bundler.render(res, 'unity', 'unity', ['client'], 'Twitter-VR');
});

app.get('/test', function(req, res, next) {
    res.sendFile(__dirname + '/static/test.html');
});

/**********************************************************************
 * EXCEPTIONS *
 **********************************************************************/
app.use(function(req, res, next){
    res.status(404);
    res.sendFile(config.getConf('PROJECTS_HOME') + '/static/shared-assets/404.html');
});

app.use(function(err, req, res, next){
    res.status(err.status || 500);
    res.sendFile(config.getConf('PROJECTS_HOME') + '/static/shared-assets/500.html');
});

/**********************************************************************
 * RUN *
 **********************************************************************/
server
    .listen(port, function(err, data) {
        logger.app.info('Started SERVER for projects/'+ project
                        +' on PORT '+ port +' '+ new Date());
    });
