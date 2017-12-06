'use strict';

/**********************************************************************
 * bundle/minify resources *
 **********************************************************************/
var project = 'twitter',
    config = require('./config'),
    Bundler = require('browserify'),
    CSS = require('clean-css'),
    hbs = require('express-handlebars');

exports.render = function(res, layout, tpl, js, title) {
    var bundler = Bundler(),
        cssBundleObj = new CSS().minify(['src/css/app.css']),
        cssBundle = cssBundleObj.styles || '',
        jsBundle = '', output;

    js.map(function(s){ bundler.add('src/js/'+ s +'.js'); });

    bundler.transform({ global: true }, 'uglifyify');
    bundler.bundle(function(err, buffer) {
        if (err) return console.log(err);

        jsBundle += buffer.toString()
            .replace('_HOST_', 'http://'+ config.getConf('NODEIP'))
            .replace('_PORT_', config.getPort(project));

        output = {
            title: title,
            css: cssBundle,
            js: jsBundle,
            layout: layout
        };

        res.render(tpl, output, function(err, content) {
            if (err) return console.log(err);
            res.send(content);
        });
    });
};
