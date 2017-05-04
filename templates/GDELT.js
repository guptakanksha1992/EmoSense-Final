/**
 * Created by akankshagupta on 5/3/17.
 */
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

function GdeltView() { //on click of GDELT button
    $.ajax({

        type: "POST",
        url: 'https://r158gk0xqk.execute-api.us-east-1.amazonaws.com/prod/GDELT_query',
        formData: {"timestamp": timestamp,
"location": [
                  latitude,
                  longitude
               ] },      
        data: JSON.stringify(formData),
        success: function(data) {
          var info = {
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

// Function to Load tweets and place them on the map
function load_tweet(list) {
	var object_list = list.hits.hits;
	console.log(JSON.stringify(object_list));
	for (var i = 0; i < object_list.length; i++) {
		curr_latitude = object_list[i]._source.location[1];
		curr_longitude = object_list[i]._source.location[0];

		//Check if the following variable is correct or not (most probably will require dominant emotion)

		dominant_emotion = max_emotion(object_list[i]._source);
		console.log('Dominant emotion is:', dominant_emotion);
		object_list[i]._source.img_source = image_emotion_mapper(dominant_emotion);
		console.log(object_list[i]._source.img_source);

		if(object_list[i]._source.sentiment == 'positive'){
			drop_marker(curr_latitude, curr_longitude, object_list[i]._source, 2);
		} else if(object_list[i]._source.sentiment == 'negative'){
			drop_marker(curr_latitude, curr_longitude, object_list[i]._source, 0);
		} else {
			drop_marker(curr_latitude, curr_longitude, object_list[i]._source, 1);
		}
	}

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

}


function get_type(thing){
    if(thing===null)return "[object Null]"; // special case
    return Object.prototype.toString.call(thing);
}

// Function to Load GDELT news variables and place them on the Carousal
function load_news(list) {
	var object_list = list.hits.hits;
	console.log(JSON.stringify(object_list));
	for (var i = 0; i < object_list.length; i++) {
		// Populate the values of the graph here
		curr_latitude = object_list[i]._source.location[1];
		curr_longitude = object_list[i]._source.location[0];
		//Check if the following variable is correct or not (most probably will require dominant emotion)
		object_list[i]._source.img_source = image_emotion_mapper(object_list[i]._source.emotion);

	}

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
// Call to lambda endpoint
        GdeltView()

	})

}