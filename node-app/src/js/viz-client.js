(function(window) {
    window.addEventListener('load', function() {


        function listen() {
            io.connect().on('twitter', function(message) {
                try {
                    data = JSON.parse(message);

                } catch (err) {
                        console.log(data);
                }
            });
        }

        window.setTimeout(listen, 3000);
    });
})(window);
