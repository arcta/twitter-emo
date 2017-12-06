'use strict';

/**********************************************************************
 * local cofiguratio paser *
 **********************************************************************/
var fs = require('fs'),
    config = {};

fs.readFileSync(process.env.HOME +'/.local.cnf')
    .toString().split('\n')
        .map(function(d) {
            if ('' !== d && '#' !== d.charAt(0) && 0 !== d.indexOf('export')) {
                var data = d.split('=');
                if (data.length > 1)
                    config[data[0]] = data[1].replace(/'/g,'').replace(/"/g,'');
            }
        });

config['PROJECT'] = {};
fs.readFileSync(process.env.HOME +'/.project.cnf')
    .toString().split('\n')
        .map(function(d) {
            if ('' !== d && '#' !== d.charAt(1)) {
                var data = d.split('\t');
                if (data.length > 1)
                    config['PROJECT'][data[1]] = {
                        'PORT':data[0].substring(data[0].length - 4),
                        'CID':data[2] };
            }
        });


config.getConf = function(key) {
    return process.env[key] || config[key];
};

config.projectConf = function(d) {
    if (d in config['PROJECT']) {
        var cnf = {};
        try {
            cnf = JSON.parse(
                fs.readFileSync(process.env.HOME +'/projects/'+ d +'/node-app/config.json')
                    .toString());
        }
        catch (err) {
            console.log('Failed loading project configuration ... '+ d +'/node-app/config.json');
        }
        finally {
            for (var k in cnf) config[k] = cnf[k];
        }
    }
};

config.getPort = function(d) {
    if (d in config['PROJECT'])
        return config['PROJECT'][d]['PORT'];
    return config.INFO_PORT;
};

module.exports = config;
