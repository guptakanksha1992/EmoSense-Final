      // Function to add HTML code to the Marker
      var map = "";
      var markerCluster;
      var marker_list = [];
      var geo_list = [];
      var infowindow = '';
      var min_zoom_level = 2;
      function image_emotion_mapper(emotion)
      {
        switch(emotion){
          case "happy": return '../static/images/happy.png';
          break;
          case "sad": return '../static/images/sad.png';
          break;
          case "angry": return '../static/images/angry.png';
          break;
          case "disgust": return '../static/images/disgust.png';
          break;
          case "fear": return '../static/images/fear.png';
          break;
          default: return '../static/images/neutral.png';

        }
      }

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

        console.log('Setting contentString to ', contentString)
        infowindow.setContent(contentString);
      }

      function initMap() {
        var nyc = {lat: 40.7128, lng: -74.0059};
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 4,
          center: nyc
        });

        var marker = new google.maps.Marker({
          position: nyc,
          map: map
        });


        infowindow = new google.maps.InfoWindow({});

        console.log('Initialized value of marker', marker);

        console.log('Initialized value of map', map);

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
          console.log('')
          toggleMarker(source_object);
          infowindow.open(map, new_marker);
        });

        marker_list.push(new_marker);
      }

      // Function to Load tweets and place them on the map
      function load_tweet(curr_latitude, curr_longitude) {

        var source_object = new Object();
        source_object.message = "Hello";
        source_object.author = "Sarang Karpate";
        source_object.timestamp = "30 Apr 2017";
        source_object.sentiment = 'positive';

        source_object.img_source = image_emotion_mapper('disgust');


        if(source_object.sentiment == 'positive'){
          drop_marker(curr_latitude, curr_longitude, source_object, 2);
        } else if(source_object.sentiment == 'negative'){
          drop_marker(curr_latitude, curr_longitude, source_object, 0);
        } else {
          drop_marker(curr_latitude, curr_longitude, source_object, 1);
        }


      }

      function search_by_geo_distance(latitude, longitude) {
        console.log('In search_by_geo_distance');
        clearMarkers();
        load_tweet(latitude, longitude);
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

      $(document).ready(function(){


        initMap();

        console.log('In the ready function');
        console.log('Value of map',map);

        a = google.maps.event.addListener(map, 'click', function(event) {
          console.log('Caught a click to the map!')
        // Once the Click has been caught, placeMarker function should be called
        placeMarker(event.latLng);
      });

        console.log(a);

      });