(function(window) {
    window.addEventListener('load', function() {
        var socket = io.connect('_HOST_:_PORT_');

        var W = window.innerWidth,
            H = window.innerHeight,
            norm = W/400,
            timer;

        var svg = d3.select('body').append('svg')
            .attr('width', W)
            .attr('height', H);

        var geo = svg.append('g')
            .attr('transform', 'translate('+ [W/2, H/2] +')');

        var cities = [
                ['London', -51.5074, -0.1278],
                ['Moscow', -55.7558, 37.6173],
                ['Los Angeles', -34.0522, -118.2437],
                ['New York', -40.7128, -74.0060],
                ['Tokyo', -35.6895, 139.6917],
                ['Beijing', -39.9042, 116.4074],
                ['Rio De Janeiro', 22.9068, -43.1729],
                ['Mexico', -19.4326, -99.1332],
                ['Nairobi', 1.2921, 36.8219],
                ['Luanda', 8.8400, 13.2894],
                ['Sydney', 33.8688, 151.2093]
            ];

        svg.append('path')
            .attr('d', 'M'+ [0, H/2] +' L'+ [W, H/2])
            .style('opacity', 0.3);

        svg.append('text')
            .attr('transform', 'translate('+ [W/2, H-10] +') rotate(-90)')
            .attr('text-anchor', 'start')
            .attr('dy', '1em')
            .text('GREENWICH')
            .style('opacity', 0.2);

        svg.append('path')
            .attr('d', 'M'+ [W/2, 0] +' L'+ [W/2, H])
            .style('opacity', 0.3);

        svg.append('text')
            .attr('transform', 'translate('+ [10, H/2] +')')
            .attr('text-anchor', 'start')
            .attr('dy', '1em')
            .text('EQUATOR')
            .style('opacity', 0.2);

        cities.map(function(d) {
            var coords = [norm * d[2], norm * d[1]];

            geo.append('circle')
                .attr('r', 4)
                .attr('transform', 'translate('+ coords +')')
                .attr('fill', '#fff')
                .attr('stroke', '#333')
                .attr('stroke-width', 2);

            geo.append('text')
                .attr('transform', 'translate('+ coords +')')
                .attr('text-anchor', 'middle')
                .attr('dy', '1.5em')
                .text(d[0]);
        });

        socket.on('connect', function(data) {
            socket.emit('join', 'Connected!');
        });

        socket.on('twitter-lang', function(message){
            //console.log(message);
        });

        socket.on('twitter-words', function(message){
            //console.log(message);
        });

        socket.on('twitter-emojis', function(message){
            //console.log(message);
        });

        socket.on('twitter-hashtags', function(message){
            //console.log(message);
        });

        socket.on('twitter-sentiment', function(message){
            //console.log(message);
        });

        socket.on('twitter-country', function(message){
            //console.log(message);
        });

        socket.on('twitter-place', function(message){
            //console.log(message);
        });

        socket.on('twitter-box', function(message){
            var data = message
                        .split(',')
                        .map(function(d){ return parseFloat(d, 10); }),
                R = 4,
                r = Math.max(R, norm * (data[2] + data[3])/2);

            geo.append('circle')
                    .attr('r', r)
                    .attr('transform', 'translate('+ [norm * data[0], -norm * data[1]] +')')
                    .attr('fill', 'hsl('+ (data[4] > 0 ? 21:210 ) +','+ (100 * Math.abs(data[4])) +'%,50%)')
                    .attr('fill-opacity', Math.exp((R - r)/10)/2)
                .transition()
                    .delay(3000)
                    .remove();
        });
    });
})(window);
