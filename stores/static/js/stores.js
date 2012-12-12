var stores = stores || {};

stores.maps = {

    overview: {
        defaultLng: -37.82850537866209,
        defaultLat: 144.9661415816081,

        init: function() {
            var map = stores.maps.createOverviewMap();
            var latLng = new google.maps.LatLng(
                stores.maps.overview.defaultLat,
                stores.maps.overview.defaultLng
            );
            var marker = new google.maps.Marker({
                position: latLng,
                map: map,
                title: 'You are here'
            });

            // init autocomplete
            var input = $('#id_store_search'),
                autocomplete = new google.maps.places.Autocomplete(input[0]);

            google.maps.event.addListener(autocomplete, 'place_changed', function () {
                var place = autocomplete.getPlace();
                stores.maps.updateMap(map, marker, place.geometry.location);
            });


            // callback function for when coordinates are found
            $('[data-behaviours~=geo-location]').live('click', function(ev) {
                ev.preventDefault();

                // get location from browser
                if (navigator.geolocation) {
                    // callback function for when location could not be determined
                    var error = function(msg) {
                        console.log("navigator.geolocation.getCurrentPosition(): error");
                        oscar.messages.error(msg);
                    };

                    var success = function(position) {
                        console.log("navigator.geolocation.getCurrentPosition(): success");
                        latLng = new google.maps.LatLng(
                            position.coords.latitude,
                            position.coords.longitude
                        );
                        // populate hidden field
                        $('#id_location').val(JSON.stringify(stores.maps.getGeoJsonFromLatLng(latLng)));

                        // update map with new marker
                        stores.maps.updateMap(map, marker, latLng);
                        console.log("#id_location (GeoJSON): " + $('#id_location').val());
                    };
                    navigator.geolocation.getCurrentPosition(success, error);
                } else {
                    oscar.messages.error('Your location could not be determined');
                }
            });

        }
    },

    updateMap: function(map, marker, latLng) {
        console.log("store.maps.updateMap()");
        var bounds = map.getBounds();
        bounds.extend(latLng);
        map.fitBounds(bounds);
        map.setCenter(latLng);
        marker.setPosition(latLng);
        var infowindow = new google.maps.InfoWindow({
            content: 'You are here'
        });
        google.maps.event.addListener(marker, "click", function() {
            infowindow.open(map, marker);
        });
    },

    getGeoJsonFromLatLng: function (latLng) {
        return {
            'type': 'Point',
            // the GeoJSON format provides latitude and longitude
            // in reverse order in the 'coordinates' list:
            // [x, y] => [longitude, latitude]
            'coordinates': [latLng.lng(), latLng.lat()]
        };
    },

    getLatLngFromGeoJSON: function (data) {
        var point = $.parseJSON(data);

        if (!point || point.type.toLowerCase() !== "point") {
            return new google.maps.LatLng(
                stores.maps.overview.defaultLat,
                stores.maps.overview.defaultLng
            );
        }

        // the GeoJSON format provides latitude and longitude
        // in reverse order in the 'coordinates' list:
        // [x, y] => [longitude, latitude]
        return new google.maps.LatLng(
            point.coordinates[1],
            point.coordinates[0]
        );
    },

    createOverviewMap: function () {
        var map = null;
        $('.store-map').each(function (elem) {
            var myOptions = {
                center: new google.maps.LatLng(-37.813988, 144.964256),
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: false,
                zoomControl: true,
                scrollwheel: true,
                zoom: 11
            };
            map = new google.maps.Map(this, myOptions);
            var bounds = new google.maps.LatLngBounds();

            $('address').each(function (elem) {
                var storeLocation = new google.maps.LatLng(
                    $(this).data('lat'),
                    $(this).data('lng')
                );
                bounds.extend(storeLocation);

                var marker = new google.maps.Marker({
                    position: storeLocation,
                    map: map,
                    title: $(this).data('name')
                });
                map.fitBounds(bounds);

                var infowindow = new google.maps.InfoWindow({
                    content: this.innerHTML
                });

                // Open the infowindow on marker click
                google.maps.event.addListener(marker, "click", function () {
                    infowindow.open(map, marker);
                });
            });

        });
        return map;
    },

    createIndividualMap: function (mapElem, addressElem, zoomLevel) {
        lat = addressElem.data('lat');
        lng = addressElem.data('lng');

        if (lat & lng) {
            storeLocation = new google.maps.LatLng(lat, lng);

            map = new google.maps.Map(mapElem, {
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: true,
                scrollwheel: false,
                zoom: zoomLevel
            });

            marker = new google.maps.Marker({
                position: storeLocation,
                map: map
            });

            map.setCenter(storeLocation);

            if (!zoomLevel) {
                bounds = new google.maps.LatLngBounds();
                bounds.extend(storeLocation);
                map.fitBounds(bounds);
                map.setCenter(bounds.getCenter());
            }

            return {
                map: map,
                location: storeLocation
            };
        }
    }
};
