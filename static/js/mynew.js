// Initialize Google map
function initMap() {

	var nyc = {lat: 40.7128, lng: -74.0059};
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 4,
		center: nyc
	});

	infowindow = new google.maps.InfoWindow({});

	console.log('Initialized value of map', map);

}

function gdeltMap(data) {
	console.log("Plotting new gdelt event markers")
  var response = data

  var Lat_sum = 0.0, Long_sum = 0.0;
  var length = response.length;

  for (i = 0; i < response.length; i++) {
      Lat_sum = Lat_sum + response[i]['ActionGeo_Lat'];
      Long_sum = Long_sum + response[i]['ActionGeo_Long'];
    }

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: new google.maps.LatLng(Lat_sum/length, Long_sum/length),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  var infowindow = new google.maps.InfoWindow();
	var marker, i;
	  var heatMapData = new Array(response.length);

	  for (i = 0; i < response.length; i++) {
	    heatMapData[i] = {location: new google.maps.LatLng(response[i]['ActionGeo_Lat'], response[i]['ActionGeo_Long']), weight: (response[i]['GoldsteinScale'])*0.1 }
	    marker = new google.maps.Marker({
	      position: new google.maps.LatLng(response[i]['ActionGeo_Lat'], response[i]['ActionGeo_Long']),
	      map: map
	    });

			marker.setOpacity(0.8);

	    google.maps.event.addListener(marker, 'click', (function(marker, i) {
	      return function() {
	        content = response[i]['SOURCEURL'];
					scale = response[i]['GoldsteinScale'];
	        content  = "<a href='" + content + "'>" + content + "</a>";
	        infowindow.setContent(content + ' GoldsteinScale is: ' + scale);
	        infowindow.open(map, marker);
	      }
	    })(marker, i));
	  }

	  var heatmap = new google.maps.visualization.HeatmapLayer({
	  data: heatMapData,
		opacity: 0.8,
		radius: 10
	  });
	  heatmap.setMap(map);
}


function gdeltquery(start_time, end_time){
	console.log('Now querying gdelt events');
	var time1 = start_time;
	var time2 = end_time;
	var newlatitude = parseFloat(geo_list[0])
	var newlongitude = parseFloat(geo_list[1])
	console.log('The lat is ', newlatitude);
	var formData = {
  timestamp: [start_time, end_time],
  location: [
    (newlatitude),
    (newlongitude)
  ]
	}
	console.log(formData)
	$.ajax({
	url: 'https://4jjj0vw665.execute-api.us-east-1.amazonaws.com/prod/delt',
	type: 'POST',
	timeout: 600000,
	tryCount : 0,
	retryLimit : 3,
	data: JSON.stringify(formData),
	contentType: "application/json; ",
	success: function(data) {
		console.log("data");
		console.log(data);
		console.log("success");
		gdeltMap(data)
	},

	error: function(error,textStatus, errorThrown){
		if (textStatus == 'timeout') {
				this.tryCount++;
				if (this.tryCount <= this.retryLimit) {
						$.ajax(this);
						return;
				}
				return;
		}
	}
});
}

// Function to add HTML code to the Marker
function toggleMarker(source_object) {
	var contentString = '<div style="float:left"><img src="'+source_object.img_source+'"></div><div style="float:right; padding: 10px;"><div id="content">'+
	'<div id="siteNotice">'+
	'</div>'+
	'<h1 id="firstHeading" class="firstHeading"></h1>'+
	'<div id="bodyContent">'+
	'<p>' + source_object.message + '</p>' +
	'<b> Author: ' + source_object.author + '</b>' +
	'<p>' + source_object.timestamp + '</p>' +
	'<b> Sentiment: ' + source_object.sentiment + '</b>' +
	'</div>'+
	'</div>';
	infowindow.setContent(contentString);
}

// Function to drop markers on Google Maps
function drop_marker(latitude, longitude, source_object, color) {
	var curr_lat_and_lng = {lat: latitude, lng: longitude};

	// Color-map {0:Red, 1:Grey, 2:Green}
	var markerColor;

	switch (color) {
		case 0:
		markerColor = 'FF0000';
		break;
		case 1:
		markerColor = 'C0C0C0';
		break;
		case 2:
		markerColor = '3AA91E';
		break;
		default:
		markerColor = 'C0C0C0';
	}

	var markerImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + markerColor,
		new google.maps.Size(80, 400),
		new google.maps.Point(0,0),
		new google.maps.Point(10, 34));


	var new_marker = new google.maps.Marker({
		position: curr_lat_and_lng,
		map: map,
		icon: markerImage
	});

	new_marker.addListener('click', function() {
		toggleMarker(source_object);
		infowindow.open(map, new_marker);
	});

	marker_list.push(new_marker);

}

function placeMarker(location) {
	clearGeoTags();
	var markerColor = '0000FF';
	var markerImage = new google.maps.MarkerImage(
		"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + markerColor,
		new google.maps.Size(80, 400),
		new google.maps.Point(0,0),
		new google.maps.Point(10, 34));
	var marker = new google.maps.Marker({
		position: location,
		map: map,
		title: "Tweets around this area",
		icon: markerImage
	});
	geo_latitude = marker.getPosition().lat();
	geo_longitude = marker.getPosition().lng();
	geo_list.push(geo_latitude);
	geo_list.push(geo_longitude);
}

function clearMarkers(){
	for (var i = 0; i < marker_list.length; i++) {
		marker_list[i].setMap(null);
	}
}

function clearGeoTags(){
	for (var i = 0; i < geo_list.length; i++) {
		geo_list[i].setMap(null);
	}
}

function limit_zoom_level() {
	google.maps.event.addListener(map, 'zoom_changed', function () {
		if (map.getZoom() < min_zoom_level) {
			map.setZoom(min_zoom_level);
		}
	});
}


var map = "";
var markerCluster;
var marker_list = [];
var geo_list = [];
var infowindow = '';
var min_zoom_level = 2;
var selected_keyword, data_series, graph_query_response;


$(document).ready(function(){

	console.log('In Javascript file');

	default_start_time = 2016;
	default_end_time = 2018;
	latitude = 40.06889420539272;
	longitude = -120.32554198435977;


	selected_keyword = 'sports';
	console.log('selected_keyword value:', selected_keyword);

	$.ajax({
		url: '/graph' +'/' + selected_keyword + '/' + default_start_time + '/' + default_end_time + '/' + latitude + '/' + longitude,
		type: 'GET',
		success: function(response) {
			console.log('In the AJAX Call')
			//console.log(JSON.stringify(response));
    		graph_query_response = response;
    		graphQueryProcessor(graph_query_response);
    	},
    	error: function(error) {
    		console.log(JSON.stringify(error));
    		$('#testing').text(JSON.stringify(error));
    	}
    });

	// Initialize Google Map
	initMap();

	a = google.maps.event.addListener(map, 'click', function(event) {
		console.log('Caught a click to the map!')
		// Once the Click has been caught, placeMarker function should be called
		placeMarker(event.latLng);
	});

	console.log(a);

	// Adding Listeners for the buttons
    //send the location in the
	document.getElementById('gdeltbutton').addEventListener('click', function (e) {
		e.preventDefault();
		clearMarkers();
		var form = document.getElementById("gdelt_form");
		start_time = form.elements['start_time'].value
		end_time = form.elements['end_time'].value
		console.log('Start time is', start_time);
		console.log('End time is', end_time);
		gdeltquery(start_time, end_time);
	}, false);

	});
