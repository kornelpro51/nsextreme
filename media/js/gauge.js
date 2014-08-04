
(function ( $ ) {
 
    $.fn.gyroscope_gauge = function(gyroscope_arr) {
		var width = 120,
		height = 120,
		twoPi = Math.PI/2-0.1,
		progress = 0,
		total = Math.max( d3.max(gyroscope_arr, function(d) { return d; }), Math.abs(Math.floor(d3.min(gyroscope_arr, function(d) { return d; }))));
		formatPercent = d3.format(".0%");


        if(total == 0) {
            total = 1;
        }

		var arc = d3.svg.arc()
			.startAngle(-Math.PI/2)
			.innerRadius(40)
			.outerRadius(50);
		var meterarc = d3.svg.arc()
			.startAngle(-Math.PI*3/2+0.1)
			.endAngle(Math.PI/2-0.1)
			.innerRadius(40)
			.outerRadius(50);
		var svg = d3.select("#"+this.attr("id")).append("svg")
			.attr("width", width)
			.attr("height", height)
			.append("g")
				.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

		var meter = svg.append("g")
			.attr("class", "gyroscope_gauge");

		meter.append("path")
			.attr("class", "background")
			.attr("d", meterarc);

		var foreground = meter.append("path")
			.attr("class", "foreground");
		var text = meter.append("text")
			.attr("text-anchor", "middle")
			.attr("dy", ".35em");
		
		var text1 = meter.append("text")
			.attr("text-anchor", "end")
			.attr("dx", "-51")
			.attr("dy", ".35em")
			.text("0");
		var text2 = meter.append("text")
			.attr("text-anchor", "start")
			.attr("dx", "51")
			.attr("dy", "-0.2em")
			.text("+");
		var text3 = meter.append("text")
			.attr("text-anchor", "start")
			.attr("dx", "52")
			.attr("dy", "0.8em")
			.text("-");
		
		this.data("gyroscope_gauge", {
			setValue : function (val, transition) {
                if (transition) {
                    var i = d3.interpolate(progress, val / total);
                    d3.transition().tween("progress", function() {
                        return function(t) {
                            progress = i(t);
                            foreground.attr("d", arc.endAngle( - Math.PI/2 + (Math.PI-0.1) * progress));
                            text.text(val);
                        };
                    });
                } else {
                    foreground.attr("d", arc.endAngle( - Math.PI/2 + (Math.PI-0.1) * val / total));
                    text.text(Math.round(val * 100) / 100);
                }
			}
		});
		return this;
	}
	$.fn.gforce_gauge = function(gforce_arr) {
		var width = 100,
		height = 100,
		progress = 0,
		total = d3.max(gforce_arr, function(d) { return d; });
		formatPercent = d3.format(".0%");
		var chartWidth = 20;

        if(total == 0) {
            total = 1;
        }

		var y = d3.scale.linear()
			.range([height, 0]);
		y.domain([0, total]);

		var svg = d3.select("#"+this.attr("id")).append("svg")
			.attr("width", width)
			.attr("height", height)
			.append("g")
				.attr("transform", "translate( 0 , 0)")
				.attr("class", "gforce_gauge");
		
		var scale = svg.selectAll(".line")
			.data(d3.range(1, 10))
			.enter().append("line")
				.attr("class", "line")
				.attr("x2", chartWidth)
				.attr("y1", function(d) {return d * height / 10;})
				.attr("y2", function(d) {return d * height / 10;});

		var bar = svg.selectAll(".bar")
			.data([{value: 3}])
			.enter().append("rect")
				.attr("class", "bar")
				.attr("opacity", "0.8")
				.attr("x", function(d) { return 0; })
				.attr("width", chartWidth)
				.attr("y", function(d) { return y(d.value); })
				.attr("height", function(d) { 
					return height - y(d.value); 
				});

		var text = svg.append("text")
			.attr("x", chartWidth + 5)
			.attr("y", height / 2)
			.attr("dy", ".35em");

		this.data("gforce_gauge", {
			setValue : function (val, transition) {
                if (transition) {
                    var i = d3.interpolate(progress, val / total);
                    d3.transition().tween("progress", function() {
                        return function(t) {
                            progress = i(t);
                            bar.attr("y", y(progress * total))
                                .attr("height" ,height - y(progress * total));
                            text.text(Math.round(progress * total * 100) / 100);
                        };
                    });
                } else {
                    bar.attr("y", y(val)).attr("height" ,height - y(val));
                    text.text(Math.round(val * 100) / 100);
                }

			}
		});
		return this;
	}
	$.fn.speed_gauge = function(speed_arr) {
		var width = 200,
		height = 120,
		twoPi = Math.PI/2,
		progress = 0,
		total = d3.max(speed_arr, function(d) { return d; }); // must be hard-coded if server doesn't report Content-Length
		formatPercent = d3.format(".0%");

        if(total == 0) {
            total = 1;
        }
        total = Math.ceil(total * 100) / 100;

		var arc = d3.svg.arc()
			.startAngle(-Math.PI/2)
			.innerRadius(80)
			.outerRadius(90);
		var meterarc = d3.svg.arc()
			.startAngle(-Math.PI/2)
			.endAngle(Math.PI/2)
			.innerRadius(80)
			.outerRadius(90);
		var svg = d3.select("#"+this.attr("id")).append("svg")
			.attr("width", width)
			.attr("height", height)
			.append("g")
				.attr("transform", "translate(" + width / 2 + "," + (height / 2 + 30) + ")");

		var meter = svg.append("g")
			.attr("class", "speed_gauge");

		meter.append("path")
			.attr("class", "background")
			.attr("d", meterarc);

		var foreground = meter.append("path")
			.attr("class", "foreground");
		var text = meter.append("text")
			.attr("text-anchor", "middle")
			.attr("class", "text1")
			.attr("dy", "0");
		var text2 = meter.append("text")
			.attr("text-anchor", "middle")
			.attr("class", "text2")
			.attr("dy", "20");
		var textStart = meter.append("text")
			.attr("text-anchor", "middle")
			.attr("class", "text3")
			.attr("dx", "-85")
			.attr("dy", "20")
			.text(0);
		var textEnd = meter.append("text")
			.attr("text-anchor", "middle")
			.attr("class", "text3")
			.attr("dx", "85")
			.attr("dy", "20")
			.text(total);

		this.data("speed_gauge", {
			setValue : function (val, transition) {

                if (transition) {
                    var i = d3.interpolate(progress, val / total);
                    d3.transition().tween("progress", function() {
                        return function(t) {
                            progress = i(t);
                            foreground.attr("d", arc.endAngle( - Math.PI/2 + (Math.PI) * progress));
                            text.text(Math.round(val * 100) / 100 + "mph");
                            text2.text(Math.round(val * 1.609343998712524801029980159176 * 100) / 100 + "kph" );
                        };
                    });
                } else {
                    foreground.attr("d", arc.endAngle( - Math.PI/2 + (Math.PI) * val / total));
                    text.text(Math.round(val * 100) / 100 + "mph");
                    text2.text(Math.round(val * 1.609343998712524801029980159176 * 100) / 100 + "kph" );
                }
			}
		});
//		mph 0.44704 m / s
//		kph 0.277777778 m / s
		return this;
	}
}( jQuery ));