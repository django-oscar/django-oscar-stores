var stores = stores || {};

stores.maps = {

    overview: {
        init: function() {
            var map = stores.maps.createOverviewMap();

            google.maps.event.addDomListener(window, 'load', function() {

                if (!!$('#id_location').val()) {
                    var location = stores.maps.getLatLngFromGeoJSON($('#id_location').val());
                    var bounds = map.getBounds();
                    bounds.extend(location);
                    map.fitBounds(bounds);

                    var marker = new google.maps.Marker({
                        position: location,
                        map: map,
                        title: 'You are here'
                    });
                    map.setCenter(location);

                    var infowindow = new google.maps.InfoWindow({
                        content: marker.title
                    });

                    // Open the infowindow on marker click
                    google.maps.event.addListener(marker, "click", function () {
                        infowindow.open(map, marker);
                    });
                }

            });

            // callback function for when coordinates are found
            var success = function(position) {

                // populate hidden field
                $('#id_location').val(
                    JSON.stringify(
                        stores.maps.getGeoJson(
                            position.coords.latitude,
                            position.coords.longitude
                        )
                    )
                );

                $('#store-search').submit();
            };

            // callback function for when location could not be determined
            var error = function(msg) {
                oscar.messages.error(msg);
            };

            $('[data-behaviours~=geo-location]').live('click', function(ev) {
                ev.preventDefault();

                // get location from browser
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(success, error);
                } else {
                    error('Your location could not be determined');
                }
            });

        }
    },

    getGeoJson: function (lat, lng) {
        return {
            'type': 'Point',
            // the GeoJSON format provides latitude and longitude
            // in reverse order in the 'coordinates' list:
            // [x, y] => [longitude, latitude]
            'coordinates': [lat, lng]
        };
    },

    getLatLngFromGeoJSON: function (data) {
        var point = jQuery.parseJSON(data);

        if (!point || point.type.toLowerCase() !== "point") {
            return new google.maps.LatLng(
                -37.82850537866209,
                144.9661415816081
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
