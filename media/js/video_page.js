
var nse_frames = nse_data_raw["frames"];
var gyroscopes = {x : [], y: [], z: []};
var accelerometer = {x : [], y: [], z: []};
var g_factor = [];
var locations = { "latitude": [], "longitude": [], "altitude": [] };
var velocity = [];
var times = [];
var distances = [];
var totalDistance = 0;
var frameLength = (typeof nse_frames == 'undefined') ? 0 : (typeof nse_frames.length == 'undefined' ? 0 : nse_frames.length);

var toHHMMSS = function (sec) {
    var sec_num = Math.round(sec); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);
    var nHours = hours;

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    if (nHours == 0) {
        return minutes+':'+seconds;
    }
    var time    = hours+':'+minutes+':'+seconds;
    return time;
}
function numberWithCommas(number) {
    var x = Math.round(number * 100) / 100;
    var parts = (x).toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}

function setVideoDetails() {
    $("#playing_moving_time").text(toHHMMSS(times[frameLength - 1]));
    if ( locations.altitude[0] - locations.altitude[frameLength - 1] < 0 ) {
        $("#playing_elevation_label").text("Elevation Gain");
        $("#playing_elevation").text((numberWithCommas(locations.altitude[frameLength - 1] - locations.altitude[0])) + "ft");
    } else {
        $("#playing_elevation_label").text("Elevation Loss");
        $("#playing_elevation").text((numberWithCommas(locations.altitude[0] - locations.altitude[frameLength - 1])) + "ft");
    }
    $("#playing_distance").text((Math.round(totalDistance * 100) / 100) + "m");
}

for (var idx = 0; idx < frameLength; idx++) {
    times.push(nse_frames[idx].time);
    gyroscopes.x.push(nse_frames[idx].gyroscope.x);
    gyroscopes.y.push(nse_frames[idx].gyroscope.y);
    gyroscopes.z.push(nse_frames[idx].gyroscope.z);

    accelerometer.x.push(nse_frames[idx].accelerometer.x);
    accelerometer.y.push(nse_frames[idx].accelerometer.y);
    accelerometer.z.push(nse_frames[idx].accelerometer.z);

    g_factor.push(Math.sqrt(
            nse_frames[idx].accelerometer.x * nse_frames[idx].accelerometer.x +
            nse_frames[idx].accelerometer.y * nse_frames[idx].accelerometer.y +
            nse_frames[idx].accelerometer.z * nse_frames[idx].accelerometer.z
        ));
    locations.latitude.push(nse_frames[idx].location.latitude);
    locations.longitude.push(nse_frames[idx].location.longitude);
    locations.altitude.push(nse_frames[idx].location.altitude);

    velocity.push(nse_frames[idx].velocity);
    if (nse_frames[idx].distance) {
        distances.push(nse_frames[idx].distance);
        totalDistance += nse_frames[idx].distance;
    }
}

$("#g_force_x").gyroscope_gauge(gyroscopes.x);
$("#g_force_y").gyroscope_gauge(gyroscopes.y);
$("#g_force_z").gyroscope_gauge(gyroscopes.z);

$("#g_factor").gforce_gauge(g_factor);
$("#g_speed").speed_gauge(velocity);

$("#g_force_x").data("gyroscope_gauge").setValue(gyroscopes.x[0]);
$("#g_force_y").data("gyroscope_gauge").setValue(gyroscopes.y[0]);
$("#g_force_z").data("gyroscope_gauge").setValue(gyroscopes.z[0]);

$("#g_factor").data("gforce_gauge").setValue(0);
$("#g_speed").data("speed_gauge").setValue(0);

setVideoDetails();

/*
RGraph.Clear($('#ch_elevation')[0]);
RGraph.ObjectRegistry.Clear();


var chElevation = new RGraph.Line('ch_elevation', locations.altitude)
        .Set('spline', true)
        .Set('numxticks', 0)
        .Set('numyticks', 0)
        .Set('hmargin', 10)
        .Set('background.grid.autofit.numvlines', 11)
        .Set('colors', ['black'])
        .Set('linewidth', 1)
        .Set('gutter.left', 40)
        .Set('gutter.right', 15)
        .Set('labels',[Math.round(times[0]),Math.round(times[picktimes]),Math.round(times[picktimes*2]), Math.round(times[picktimes*3]), Math.round(times[nse_frames.length-1])])
        .Set('shadow',false)
        .Set('shadow.color','#aaa')
        .Set('shadow.blur',1)
        .Set('tooltips', ['aaa', 'Fred', 'Jane', 'Lou', 'Pete', 'Kev'])
        .Set('colors', ['green'])
        .Set('tickmarks', 'circle')
        .Draw();

var chFactor = new RGraph.Line('ch_factor', g_factor)
        .Set('spline', true)
        .Set('numxticks', 0)
        .Set('numyticks', 0)
        .Set('hmargin', 10)
        .Set('background.grid.autofit.numvlines', 11)
        .Set('colors', ['black'])
        .Set('linewidth', 1)
        .Set('gutter.left', 40)
        .Set('gutter.right', 15)
        .Set('labels',[Math.round(times[0]),Math.round(times[picktimes]),Math.round(times[picktimes*2]), Math.round(times[picktimes*3]), Math.round(times[nse_frames.length-1])])
        .Set('shadow',false)
        .Set('shadow.color','#aaa')
        .Set('shadow.blur',1)
        .Set('tooltips', ['aaa', 'Fred', 'Jane', 'Lou', 'Pete', 'Kev'])
        .Set('colors', ['green'])
        .Set('tickmarks', 'circle')
        .Draw();

var chSpeed = new RGraph.Line('ch_speed', velocity)
        .Set('spline', true)
        .Set('numxticks', 0)
        .Set('numyticks', 0)
        .Set('hmargin', 10)
        .Set('background.grid.autofit.numvlines', 11)
        .Set('colors', ['black'])
        .Set('linewidth', 1)
        .Set('gutter.left', 40)
        .Set('gutter.right', 15)
        .Set('labels',[Math.round(times[0]),Math.round(times[picktimes]),Math.round(times[picktimes*2]), Math.round(times[picktimes*3]), Math.round(times[nse_frames.length-1])])
        .Set('shadow',false)
        .Set('shadow.color','#aaa')
        .Set('shadow.blur',1)
        .Set('tooltips', ['aaa', 'Fred', 'Jane', 'Lou', 'Pete', 'Kev'])
        .Set('colors', ['green'])
        .Set('tickmarks', 'circle')
        .Draw();

*/
var tickInterval = Math.floor(frameLength / 4);
var highchartCommonOption = {
    title: {
        text: null
    },
    exporting: {
        enabled: false
    },
    xAxis: {
        tickInterval: tickInterval,
        title: {
            enabled: false
        }
    },
    yAxis: {
        title: {
            text: null
        }
    },
    tooltip: {
        shared: false,
        useHTML: true,
        headerFormat: '<small>{point.key:.2f}s</small><table>',
        pointFormat: '<tr><td style="color: {series.color}">{series.name}: </td>' +
        '<td style="text-align: right"><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        valueDecimals: 2
    },
    legend: {
        enabled: false
    },
    plotOptions: {
        areaspline: {
            fillColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                stops: [
                    [0, Highcharts.Color("#A4F632").setOpacity(0.5).get('rgba')],
                    [1, Highcharts.Color("#A4F632").setOpacity(0.5).get('rgba')]
                ]
            },
            lineWidth: 2,
            marker: {
                enabled: false
            },
            shadow: false,
            states: {
                hover: {
                    lineWidth: 2
                }
            },
            threshold: null
        }
    }
};
//var elevationOption =  = gfactorOption = speedOption = {};
var elevationOption = $.extend({}, highchartCommonOption,
    {
        chart: {
            renderTo: 'ch_elevation_d',
            zoomType: 'x',
            spacingRight: 20
        },
        xAxis: { categories: times,
            tickInterval: tickInterval,
            title: {
                enabled: false
            },
            labels:{
                format: "{value:.2f}s"
            }
        },
        series: [{
            type: 'areaspline',
            name: 'Elevation',
            color: "#A4F632",
            data: locations.altitude
        }]
    });
var gfactorOption = $.extend({},highchartCommonOption,
    {
        chart: {
            renderTo: 'ch_factor_d',
            zoomType: 'x',
            spacingRight: 20
        },
        xAxis: { categories: times,
            tickInterval: tickInterval,
            title: {
                enabled: false
            },
            labels:{
                format: "{value:.2f}s"
            }
        },
        series: [{
            type: 'areaspline',
            name: 'g-factor',
            data: g_factor
        }],
        plotOptions: {
            areaspline: {
                fillColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0.4).get('rgba')],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0.4).get('rgba')]
                    ]
                },
                lineWidth: 2,
                marker: {
                    enabled: false
                },
                shadow: false,
                states: {
                    hover: {
                        lineWidth: 2
                    }
                },
                threshold: null
            }
        }
    });

var speedOption = $.extend({}, highchartCommonOption,
    {
        chart: {
            renderTo: 'ch_speed_d',
            zoomType: 'x',
            spacingRight: 20
        },
        xAxis: { categories: times,
            tickInterval: tickInterval,
            title: {
                enabled: false
            },
            labels:{
                format: "{value:.2f}s"
            }
        },
        series: [{
            type: 'areaspline',
            name: 'Speed',
            color: "#0000FF",
            data: velocity
        }],
        plotOptions: {
            areaspline: {
                fillColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, Highcharts.Color("#000000").setOpacity(1).get('rgba')],
                        [1, Highcharts.Color("#0B24FB").setOpacity(1).get('rgba')]
                    ]
                },
                lineWidth: 1,
                marker: {
                    enabled: false
                },
                shadow: false,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        }
    });
//$('#ch_elevation_d').highcharts(elevationOption);
//$('#ch_factor_d').highcharts(gfactorOption);
//$('#ch_speed_d').highcharts(speedOption);

var elevationChart = new Highcharts.Chart(elevationOption);
var factorChart = new Highcharts.Chart(gfactorOption);
var speedChart = new Highcharts.Chart(speedOption);


var map, layer, lineLayer;
    function initMap(){
			var extent= new OpenLayers.Bounds(-13,25,49,60).transform( fromProjection, toProjection);

            map = new OpenLayers.Map();

			layer = new OpenLayers.Layer.OSM( "Simple OSM Map");
			lineLayer = new OpenLayers.Layer.Vector("Line Layer");
			map.addLayer(layer);

			//map.addControl(new OpenLayers.Control.DrawFeature(lineLayer, OpenLayers.Handler.Path));
			var fromProjection = new OpenLayers.Projection("EPSG:4326");
			var toProjection   = new OpenLayers.Projection("EPSG:900913");

			var centerLat = 44.61325550921691;
			var centerLng = -123.358995868008;
            if ( frameLength > 0) {
                centerLat = (locations.latitude[frameLength - 1] + locations.latitude[0]) / 2;
                centerLng = (locations.longitude[frameLength - 1] + locations.longitude[0]) / 2;
            }
			map.addLayer(lineLayer);

			map.setCenter( new OpenLayers.LonLat(centerLng, centerLat).transform( fromProjection, toProjection), 14 );

			var points = [];
            for (i = 0; i < frameLength; i++ ) {
                points.push( new OpenLayers.Geometry.Point(locations.longitude[i], locations.latitude[i]).transform( fromProjection, toProjection) );
            }
			var line = new OpenLayers.Geometry.LineString(points);

			var style = {
				strokeColor: '#0000ff',
				strokeOpacity: 1,
				strokeWidth: 2
			};

			var lineFeature = new OpenLayers.Feature.Vector(line, null, style);
			lineLayer.addFeatures([lineFeature]);
            /*
            layer = new OpenLayers.Layer.OSM( "Simple OSM Map");
			lineLayer = new OpenLayers.Layer.Vector("Line Layer");
			map.addLayer(layer);

			//map.addControl(new OpenLayers.Control.DrawFeature(lineLayer, OpenLayers.Handler.Path));
			var fromProjection = new OpenLayers.Projection("EPSG:4326");
			var toProjection   = new OpenLayers.Projection("EPSG:900913");

			var centerLat = 44.61325550921691;
			var centerLng = -123.358995868008;

			//if (typeof locations.latitude.length != "undefined" && locations.latitude.length > 0) {
			//    centerLat = (locations.latitude[locations.latitude.length - 1] + locations.latitude[0]) / 2;
			//    centerLng = (locations.longitude[locations.latitude.length - 1] + locations.longitude[0]) / 2;
			//}

			map.addLayer(lineLayer);

			//map.addControl(new OpenLayers.Control.LayerSwitcher());
			//map.addControl(new OpenLayers.Control.MousePosition());

			map.setCenter( new OpenLayers.LonLat(centerLng, centerLat).transform( fromProjection, toProjection), 13 );

			var points = new Array(
				new OpenLayers.Geometry.Point(-123.3522271459208, 44.62985184513463).transform( fromProjection, toProjection),
				new OpenLayers.Geometry.Point(-123.358995868008, 44.61325550921691).transform( fromProjection, toProjection)
			);
			var line = new OpenLayers.Geometry.LineString(points);

			var style = {
				strokeColor: '#0000ff',
				strokeOpacity: 1,
				strokeWidth: 1
			};

			var lineFeature = new OpenLayers.Feature.Vector(line, null, style);
			lineLayer.addFeatures([lineFeature]);

			var bounds = new OpenLayers.Bounds();
			bounds.extend(new OpenLayers.LonLat(-123.3522271459208, 44.62985184513463).transform( fromProjection, toProjection));
			bounds.extend(new OpenLayers.LonLat(-123.358995868008, 44.61325550921691).transform( fromProjection, toProjection));
            */
			//var bounds = new OpenLayers.Bounds();
			//bounds.extend(new OpenLayers.LonLat(-123.3522271459208, 44.62985184513463).transform( fromProjection, toProjection));
			//bounds.extend(new OpenLayers.LonLat(-123.358995868008, 44.61325550921691).transform( fromProjection, toProjection));
        }
$('.activity_tab  a[href="#detail-map"]').click(function(){
    setTimeout(function(){
        //google.maps.event.trigger(map, 'resize');
        //layer.redraw();
        //lineLayer.redraw();
        map.render("map-canvas");
    }, 100)
});
$("#btn_create_comment").click(function(e){
    $.ajax({
        url: "/comment/create/" + VIDEOID + "/",
        data: {'content': $("#txt_create_comment").val()
        },
        method: "post",
        success: function(result) {
            console.log(arguments);
            if(result.success == true) {
                $("#recent_comments").html(result.recent);
                $("#top_comments").html(result.top);
            }
        },
        failed: function() {
            console.log(arguments);
        }
    });
});
$(".comment-tab").delegate("a.like", "click", function(e){
    var evt = e ? e: window.event;
    evt.preventDefault();
    var commentId = $(this).attr('href');
    $.ajax({
        url: "/comment/vote/" + commentId + "/",
        data: {
            'mode': "like"
        },
        method: "post",
        success: function(result) {
            console.log(arguments);
            if(result.success == true) {
                $(".c_recommend_"+commentId).html(result.recommend);
            }
        },
        failed: function() {
            console.log(arguments);
        }
    });
    return false;
});
$(".comment-tab").delegate("a.unlike", "click", function(e){
    var evt = e ? e: window.event;
    evt.preventDefault();
    var commentId = $(this).attr('href');
    $.ajax({
        url: "/comment/vote/" + commentId + "/",
        data: {
            'mode': "unlike"
        },
        method: "post",
        success: function(result) {
            console.log(arguments);
            if(result.success == true) {
                $(".c_recommend_"+commentId).html(result.recommend);
            }
        },
        failed: function() {
            console.log(arguments);
        }
    });
    return false;
});
function findIdxInTime(t) {
    for(var i = 0; i < frameLength; i++ ) {
        if(times[i] > t) {
            return i;
        }
    }
    return frameLength - 1;
}

$(document).ready(function(){
    initMap();
    var playerAPI = $(".flowplayer:first").data("flowplayer");
    playerAPI.bind("progress", function(e, api, time) {
        // do your thing
        var idx = findIdxInTime(time);
        $("#g_force_x").data("gyroscope_gauge").setValue(gyroscopes.x[idx]);
        $("#g_force_y").data("gyroscope_gauge").setValue(gyroscopes.y[idx]);
        $("#g_force_z").data("gyroscope_gauge").setValue(gyroscopes.z[idx]);

        $("#g_factor").data("gforce_gauge").setValue(g_factor[idx]);
        $("#g_speed").data("speed_gauge").setValue(velocity[idx]);

        if (idx > 0) {
            elevationChart.series[0].data[idx-1].setState();
            elevationChart.tooltip.hide();

            factorChart.series[0].data[idx-1].setState();
            factorChart.tooltip.hide();

            speedChart.series[0].data[idx-1].setState();
            speedChart.tooltip.hide();
        }

        elevationChart.series[0].data[idx].setState('hover');
        elevationChart.tooltip.refresh(elevationChart.series[0].data[idx], times[idx]);

        factorChart.series[0].data[idx].setState('hover');
        factorChart.tooltip.refresh(factorChart.series[0].data[idx], times[idx]);

        speedChart.series[0].data[idx].setState('hover');
        speedChart.tooltip.refresh(speedChart.series[0].data[idx], times[idx]);
    });
    playerAPI.bind("seek", function(e, api, time) {
       // do your thing
        var idx = findIdxInTime(time);
        $("#g_force_x").data("gyroscope_gauge").setValue(gyroscopes.x[idx]);
        $("#g_force_y").data("gyroscope_gauge").setValue(gyroscopes.y[idx]);
        $("#g_force_z").data("gyroscope_gauge").setValue(gyroscopes.z[idx]);

        $("#g_factor").data("gforce_gauge").setValue(g_factor[idx]);
        $("#g_speed").data("speed_gauge").setValue(velocity[idx]);

        if (idx > 0) {
            elevationChart.series[0].data[idx-1].setState();
            elevationChart.tooltip.hide();

            factorChart.series[0].data[idx-1].setState();
            factorChart.tooltip.hide();

            speedChart.series[0].data[idx-1].setState();
            speedChart.tooltip.hide();
        }

        elevationChart.series[0].data[idx].setState('hover');
        elevationChart.tooltip.refresh(elevationChart.series[0].data[idx], times[idx]);

        factorChart.series[0].data[idx].setState('hover');
        factorChart.tooltip.refresh(factorChart.series[0].data[idx], times[idx]);

        speedChart.series[0].data[idx].setState('hover');
        speedChart.tooltip.refresh(speedChart.series[0].data[idx], times[idx]);
    });
    playerAPI.bind("resume", function() {
        if( $(".btn-expand").data("expanded") == "False" ) {
            $("#video_info_area").hide();
            $("#video_player_area").removeClass("span6").addClass("span10");
            $(".btn-expand").data("expanded", "True");
            $(".btn-expand").find('i').removeClass('icon-backward').addClass('icon-forward');
            playerAPI.unload();
            $(".flowplayer").css({width: 680, height: 480});
            playerAPI.load(VIDEOURL, function() {
                playerAPI.play();
            });
            $(".flowplayer").removeClass('is-seeking');
        }
    });
    playerAPI.bind("finish", function() {
        if( $(".btn-expand").data("expanded") == "True" ) {
            $("#video_info_area").show();
            $("#video_player_area").removeClass("span10").addClass("span6");
            $(".btn-expand").data("expanded", "False");
            $(".btn-expand").find('i').removeClass('icon-forward').addClass('icon-backward');
            playerAPI.unload();
            $(".flowplayer").css({width: 362, height: 288});
            playerAPI.load();
            $(".flowplayer").removeClass('is-seeking');
        }
    });
    $(".btn-expand").click(function(){
        if( $(this).data("expanded") == "False" ) {
            $("#video_info_area").hide();
            $("#video_player_area").removeClass("span6").addClass("span10");
            $(this).data("expanded", "True");
            $(this).find('i').removeClass('icon-backward').addClass('icon-forward');
            playerAPI.unload();
            $(".flowplayer").css({width: 680, height: 480});
            playerAPI.load();
            $(".flowplayer").removeClass('is-seeking');
        } else {
            $("#video_info_area").show();
            $("#video_player_area").removeClass("span10").addClass("span6");
            $(this).data("expanded", "False");
            $(this).find('i').removeClass('icon-forward').addClass('icon-backward');
            playerAPI.unload();
            $(".flowplayer").css({width: 362, height: 288});
            playerAPI.load();
            $(".flowplayer").removeClass('is-seeking');
        }
    });
});

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
function shareEmail() {
    var email = document.getElementById("share-email-address").value;
    // submit to server
    var jqxhr = $.post('/video/'+VIDEOID+'/share_via_email', { email: email }, function(data) {
        if (data.errors) {
            $("div.errors").empty().append(data.errors);
            $("div.errors").show();
        } else {
            closeDialog();
        }
    });
    jqxhr.error(function(jqXHR, status, thrownError) {
        $("div.errors").empty().append(thrownError);
        $("div.errors").show();
    });
}
function closeDialog () {
    $("div.errors").empty().append('none').hide();
    document.getElementById("share-email-address").value = '';
    $('#shareEmailDialog').modal('hide');
}