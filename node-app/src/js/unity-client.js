(function(window) {
    window.addEventListener('load', function() {

        function listen() {
            io.connect().on('twitter', function(message) {

                if (typeof(SendMessage) === 'function') {
                    //handle pubsub
                }
            });
        }

        window.setTimeout(listen, 3000); //give it time to load
    });
})(window);
