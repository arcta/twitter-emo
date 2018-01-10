(function(window) {
    window.addEventListener('load', function() {

        function listen() {
            io.connect().on('twitter', function(message) {
                if (typeof(SendMessage) === 'function') {
                    var args = {}, data, geo, words;

                    try {
                        data = JSON.parse(message);

                        geo = 'country' in data ? (data['country'] === 'US' ? 1 : 2) : 0;

                        tags = Object.keys(data['tags']);

                        args = {
                            'lang': data['lang'].toLowerCase(),
                            'text': data['text'],
                            'bin': geo
                        };

                        if (words.length && data['lang'] === 'en')
                            args['words'] = words;

                    } catch (err) {
                        console.log(data);
                    }

                    if ('lang' in args)
                        SendMessage('Twitter Listener', 'Bar', '' + args['lang']);

                    if ('bin' in args)
                        SendMessage('Twitter Listener', 'Bin', args['bin'] + ',' + args['lang']);

                    if ('tags' in args)
                        SendMessage('Twitter Listener', 'Cloud', args['tags'].join(',').toLowerCase());

                    //if ('words' in args)
                    //    SendMessage('Twitter Listener', 'Words', args['words'].join(','));

                    //if ('text' in args)
                    //    SendMessage('Twitter Listener', 'Content', args['text']);
                }
            });
        }

        window.setTimeout(listen, 3000);
    });
})(window);
