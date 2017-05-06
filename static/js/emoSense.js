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

function image_emotion_mapper(emotion)
{
	switch(emotion){
		case "happy": return '/static/images/happy.png';
		break;
		case "sad": return '/static/images/sad.png';
		break;
		case "angry": return '/static/images/angry.png';
		break;
		case "disgust": return '/static/images/disgust.png';
		break;
		case "fear": return '/static/images/fear.png';
		break;
		default: return '/static/images/neutral.png';

	}
}

// Function to calculate the dominant emotion for a tweet
function max_emotion(object){
	//console.log(object);

	var happy_value, sad_value, angry_value, disgust_value, fear_value;

	happy_value = object.joy;
	sad_value = object.sadness;
	angry_value = object.anger;
	disgust_value = object.disgust;
	fear_value = object.fear;

	console.log('Emotion variables',happy_value, sad_value, angry_value, disgust_value, fear_value);
	switch(Math.max(happy_value, sad_value, angry_value, disgust_value, fear_value)){
		case happy_value: return 'happy';
		break;
		case sad_value: return 'sad';
		break;
		case angry_value: return 'angry';
		break;
		case disgust_value: return 'disgust';
		break;
		case fear_value: return 'fear';
		break;
		default: return 'no max value';
		break;
	}

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
	search_by_geo_distance(geo_latitude, geo_longitude);
}


function get_type(thing){
    if(thing===null)return "[object Null]"; // special case
    return Object.prototype.toString.call(thing);
}

// Function to clear the News Articles carousal
function clear_news(){
	for (var i = 0; i < 6; i++) {

		//Changing the title
		document.getElementById("title-" + String(i + 1)).innerHTML = "";

		//Changing the Link
		document.getElementById("link-" + String(i + 1)).href="";

		//Changing the Image
		document.getElementById("img-" + String(i + 1)).src = "";
		
	}
}

// Function to Load news variables and place them on the Carousal
function load_news(list) {
	var object_list = list.hits.hits;
	var processed_object_list = [];
	var titles_selected = [];

	for (var i = 0; i < object_list.length; i++) {
		console.log('Object Number', i + 1);
		console.log(object_list[i]._source.title);
		console.log('------');
		}

		
	// Randomly select 6 non-repeating news articles
	if(object_list.length <= 6){
		processed_object_list = object_list;
	}else {
		while(processed_object_list.length < 6){
			i = Math.floor((Math.random() * object_list.length) + 0);
			/*	if(titles_selected.indexOf(object_list[i]._source.title) <= -1){
				console.log('Adding to processed_object_list')
				processed_object_list.push(object_list[i]);
				titles_selected.push(object_list[i]._source.title);
				console.log('Title list untill now');
				console.log(titles_selected);
			}*/
			processed_object_list.push(object_list[i]);
		}
	}

	console.log('--*****--')
	
	for (var i = 0; i < processed_object_list.length; i++) {

		//Changing the title
		document.getElementById("title-" + String(i + 1)).innerHTML = processed_object_list[i]._source.title;

		//Changing the Link
		document.getElementById("link-" + String(i + 1)).href=processed_object_list[i]._source.url;

		//Changing the Image
		document.getElementById("img-" + String(i + 1)).src = processed_object_list[i]._source.url2image;
		
	}

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

    // This Ajax call is for populating the Graph
    $.ajax({
    	url: '/graph' +'/' + selected_keyword + '/' + default_start_time + '/' + default_end_time + '/' + latitude + '/' + longitude,
    	type: 'GET',
    	success: function(response) {
    		console.log('In the AJAX Call for Graphs')
    		console.log('Querying start time:', default_start_time, 'End time:', default_end_time, 'latitude:', latitude, 'longitude:', longitude);
    		console.log(JSON.stringify(response));
    		graph_query_response = response;
    		graphQueryProcessor(graph_query_response);
    	},
    	error: function(error) {
    		console.log(JSON.stringify(error));
    		$('#testing').text(JSON.stringify(error));
    	}
    });


    // This Ajax call is for populating the News Carousal
    $.ajax({
    	url: '/news' +'/' + selected_keyword + '/' + default_start_time + '/' + default_end_time + '/' + latitude + '/' + longitude,
    	type: 'GET',
    	success: function(response) {
    		load_news(response);
    	},
    	error: function(error) {
    		console.log(JSON.stringify(error));
    		$('#testing').text(JSON.stringify(error));
    	}
    });

}

function search_by_keyword(selected_keyword) {
    //Here is where the ajax call is made i.e. where we then call the endpoint associated with the search function
    console.log(selected_keyword);
    $.ajax({
    	url: '/search/' + selected_keyword,
    	type: 'GET',
    	success: function(response) {
    		load_tweet(response);
    	},
    	error: function(error) {
    		console.log(JSON.stringify(error));
    		$('#testing').text(JSON.stringify(error));
    	}
    });
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

// Function for rendering a graph
function graphRenderer(data_series, data_series2, data_series3, data_series4, data_series5){

	Highcharts.chart('graph', {

		title: {
			text: 'Emotion Values'
		},

		xAxis: {
			tickInterval: 7 * 24 * 3600 * 1000, // one week
            tickWidth: 0,
            gridLineWidth: 1,
			type: 'datetime',
			dateTimeLabelFormats: {
	           day: '%Y %b %d'    //ex- 01 Jan 2016
	       },

	       gridLineWidth: 1,
	       title: {
	       	text: 'Days'
	       },
	       labels: {
	       	align: 'left',
	       	x: 3,
	       	y: -3
	       }
	   },

        yAxis: [{ // left y axis
        	title: {
        		text: 'Score'
        	},
        	labels: {
        		align: 'left',
        		x: 3,
        		y: 16,
        		format: '{value:.,0f}'
        	},
        	showFirstLabel: false
        }, { // right y axis
        	linkedTo: 0,
        	gridLineWidth: 0,
        	opposite: true,
        	title: {
        		text: null
        	},
        	labels: {
        		align: 'right',
        		x: -3,
        		y: 16,
        		format: '{value:.,0f}'
        	},
        	showFirstLabel: false
        }],

        legend: {
        	align: 'center',
        	verticalAlign: 'top',
        	y: 20,
        	floating: true,
        	borderWidth: 0
        },

        tooltip: {
        		// Pointer basically spans all the values of a given day
        		shared: true,
        		crosshairs: true
        	},

        	plotOptions: {
        		series: {
        			cursor: 'pointer',
        			point: {
        				events: {
                    		// Event to understand what happens when a point is clicked
                    		click: function (e) {
                    			hs.htmlExpand(null, {
                    				pageOrigin: {
                    					x: e.pageX || e.clientX,
                    					y: e.pageY || e.clientY
                    				},
                    				headingText: this.series.name,
                    				maincontentText: Highcharts.dateFormat('%A, %b %e, %Y', this.x) + ':<br/> ' + 'Score:' +
                    				this.y,
                    				width: 200
                    			});
                    		}
                    	}
                    },
                    marker: {
                    	lineWidth: 1
                    }
                }
            },

            series: [{
            	data: data_series,
            	name: 'Joy',
            	lineWidth: 4,
            	marker: {
            		radius: 4
            	}
            }, {
            	data: data_series2,
            	name: 'Sad',
            	lineWidth: 4,
            	marker: {
            		radius: 4
            	}
            }, {
            	data: data_series3,
            	name: 'Angry',
            	lineWidth: 4,
            	marker: {
            		radius: 4
            	}
            }, {
            	data: data_series4,
            	name: 'Disgust',
            	lineWidth: 4,
            	marker: {
            		radius: 4
            	}
            }, {
            	data: data_series5,
            	name: 'Fear',
            	lineWidth: 4,
            	marker: {
            		radius: 4
            	}
            }
            ]
        });

	
}

// Function to map the months to an integer value
function month_mapper(month_word){
	switch(month_word){
		case 'Jan': return 1;
		case 'Feb': return 2;
		case 'Mar': return 3;
		case 'Apr': return 4;
		case 'May': return 5;
		case 'Jun': return 6;
		case 'Jul': return 7;
		case 'Aug': return 8;
		case 'Sep': return 9;
		case 'Oct': return 10;
		case 'Nov': return 11;
		case 'Dec': return 12;
	}
}

// Function for processing a Graph Query Response
function graphQueryProcessor(graph_query_response){

	// Order: Joy, Anger, Sadness, disgust, Fear Series 

	console.log('First data series', graph_query_response['collated_emotions'][0]);

	var joy_series = [];
	for (x in graph_query_response['collated_emotions'][0]){
		year = parseInt(x.substring(0,4));
		day = parseInt(x.slice(-2));
		var monthReg = /(\D)+/;
		month_word = x.match(monthReg)[0];
		month = month_mapper(month_word);
		value = (graph_query_response['collated_emotions'][0][x]);
		console.log('Year:',year, 'Month', month, 'Day:', day, 'Value:', value);
		joy_series.push([Date.UTC(year,month - 1,day),value])

	}

	var anger_series = [];
	for (x in graph_query_response['collated_emotions'][1]){
		year = parseInt(x.substring(0,4));
		day = parseInt(x.slice(-2));
		var monthReg = /(\D)+/;
		month_word = x.match(monthReg)[0];
		month = month_mapper(month_word);
		value = (graph_query_response['collated_emotions'][1][x]);
		console.log('Year:',year, 'Month', month, 'Day:', day, 'Value:', value);
		anger_series.push([Date.UTC(year,month - 1,day),value])

	}

	var sadness_series = [];
	for (x in graph_query_response['collated_emotions'][2]){
		year = parseInt(x.substring(0,4));
		day = parseInt(x.slice(-2));
		var monthReg = /(\D)+/;
		month_word = x.match(monthReg)[0];
		month = month_mapper(month_word);
		value = (graph_query_response['collated_emotions'][2][x]);
		console.log('Year:',year, 'Month', month, 'Day:', day, 'Value:', value);
		sadness_series.push([Date.UTC(year,month - 1,day),value])

	}

	var disgust_series = [];
	for (x in graph_query_response['collated_emotions'][3]){
		year = parseInt(x.substring(0,4));
		day = parseInt(x.slice(-2));
		var monthReg = /(\D)+/;
		month_word = x.match(monthReg)[0];
		month = month_mapper(month_word);
		value = (graph_query_response['collated_emotions'][3][x]);
		console.log('Year:',year, 'Month', month, 'Day:', day, 'Value:', value);
		disgust_series.push([Date.UTC(year,month - 1,day),value])

	}


	var fear_series = [];
	for (x in graph_query_response['collated_emotions'][4]){
		year = parseInt(x.substring(0,4));
		day = parseInt(x.slice(-2));
		var monthReg = /(\D)+/;
		month_word = x.match(monthReg)[0];
		month = month_mapper(month_word);
		value = (graph_query_response['collated_emotions'][4][x]);
		console.log('Year:',year, 'Month', month, 'Day:', day, 'Value:', value);
		fear_series.push([Date.UTC(year,month - 1,day),value])

	}

	graphRenderer(joy_series, sadness_series, anger_series, disgust_series, fear_series);

}

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

	$.ajax({
    	url: '/news' +'/' + selected_keyword + '/' + default_start_time + '/' + default_end_time + '/' + latitude + '/' + longitude,
    	type: 'GET',
    	success: function(response) {
    		load_news(response);
    	},
    	error: function(error) {
    		console.log(JSON.stringify(error));
    		$('#testing').text(JSON.stringify(error));
    	}
    });

	document.getElementById('sports').addEventListener('click', function (e) {
		e.preventDefault();
		clearMarkers();
		selected_keyword = this.id;
		search_by_keyword(selected_keyword);

	}, false);

	document.getElementById('politics').addEventListener('click', function (e) {
		e.preventDefault();
		clearMarkers();
		selected_keyword = this.id;
		search_by_keyword(selected_keyword);

	}, false);

	document.getElementById('technology').addEventListener('click', function (e) {
		e.preventDefault();
		clearMarkers();
		selected_keyword = this.id;
		search_by_keyword(selected_keyword);

	}, false);

	document.getElementById('health').addEventListener('click', function (e) {
		e.preventDefault();
		clearMarkers();
		selected_keyword = this.id;
		search_by_keyword(selected_keyword);

	}, false);

	document.getElementById('entertainment').addEventListener('click', function (e) {
		e.preventDefault();
		clearMarkers();
		selected_keyword = this.id;
		console.log('Keyword selected:', selected_keyword);
		search_by_keyword(selected_keyword);

	}, false);

	document.getElementById('keyword_select_form').addEventListener('submit', function (e) {
		e.preventDefault();
		clearMarkers();
		var form = document.getElementById("keyword_select_form");
		selected_keyword = form.elements['search_keyword'].value
		console.log('Keyword selected:', selected_keyword);
		search_by_keyword(selected_keyword);

	}, false);
	
});