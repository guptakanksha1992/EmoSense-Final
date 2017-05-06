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



function GdeltView(timestamp, latitude, longitude) {
	var formData = {"timestamp": timestamp,
						"location": [
	                  latitude,
	                  longitude
	               ] } //on click of GDELT button
$.ajax({

		// CODE FOR JAVASCRIPT ---NACHIKET

		/*$.ajax({
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
    });*/

        url: 'https://4jjj0vw665.execute-api.us-east-1.amazonaws.com/prod/delt',
        type: "POST",
              
				data: JSON.stringify(formData),
				contentType: "application/json; charset=utf-8",
        success: function(data) {
				data = JSON.parse(data);
				console.log("data");
				console.log(data);
				console.log("success");
    // plot data on map
          };
        },

        error: function (data) {

            alert("Could not load GDELT view!!");

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
	geo_list.push(marker);
	search_by_geo_distance(geo_latitude, geo_longitude);
}


function get_type(thing){
    if(thing===null)return "[object Null]"; // special case
    return Object.prototype.toString.call(thing);
}


function search_by_geo_distance(latitude, longitude) {
	clearMarkers();
	clear_news();
	console.log('In search_by_geo_distance function');
	console.log('selected_keyword global variable\'s value:', selected_keyword);
	var selected_key = selected_keyword;
	var selected_distance = 1000;
    //Here is where the ajax call is made i.e. where we then call the endpoint associated with the search function
    console.log('Selected Distance:',selected_distance);
    // This Ajax call is for populating the tweets
    $.ajax({
    	url: '/search/' + selected_keyword + '/' + selected_distance + '/' + latitude + '/' + longitude,
    	type: 'GET',
    	success: function(response) {
    		console.log(JSON.stringify(response));
    		load_tweet(response);
    	},
    	error: function(error) {
    		console.log(JSON.stringify(error));
    		$('#testing').text(JSON.stringify(error));
    	}
    });

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

$(document).ready(function(){

	console.log('In Javascript GDELT file');

	default_start_time = 20150111;
	default_end_time = 20180101;
	latitude = 40.06889420539272;
	longitude = -120.32554198435977;

	// Initialize Google Map
	initMap();

	a = google.maps.event.addListener(map, 'click', function(event) {
		console.log('Caught a click to the map!')
		// Once the Click has been caught, placeMarker function should be called
		placeMarker(event.latLng);
	});

	console.log(a);
	GdeltView(default_start_time, default_end_time, latitude, longitude);

	// Adding Listeners for the buttons
	document.getElementById('gdeltbutton').addEventListener('click', function (e) {
		e.preventDefault();
		clearMarkers();
		var form = document.getElementById("keyword_select_form");
		selected_keyword = form.elements['search_keyword'].value
    // Call to lambda endpoint
        GdeltView(default_start_time, default_end_time, latitude, longitude);

	})

}
