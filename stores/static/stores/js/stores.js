var stores = stores || {};

stores.maps = {

    overview: {
        init: function(marker) {
            var map = stores.maps.overview.createOverviewMap(marker);
            stores.maps.overview.initAutocomplete();
            stores.maps.overview.initGeoLocation();

            // Submit form when a user selects a store type
            $('[data-behaviours~=filter-group]').on('change', function () {
                $('#store-search').submit();
            });
        },

        initAutocomplete: function() {
            var input = $('#id_query'),
                autocomplete = new google.maps.places.Autocomplete(input[0]);

            // 'placed_changed' event fires when a user selects a place from the
            // autocomplete predictions.  We update the hidden location input with
            // a geo-json version of the LatLng and submit the form after a short delay.
            google.maps.event.addListener(autocomplete, 'place_changed', function() {
                var place = autocomplete.getPlace();
                if (place.geometry) {
                    stores.maps.overview.updateLocation(place.geometry.location);
                    $('#store-search').submit();
                }
            });
        },

        initGeoLocation: function() {
            $('[data-behaviours~=geo-location]').live('click', function (ev) {
                if (navigator.geolocation) {
                    // Define callbacks for error/success
                    var error = oscar.messages.error;
                    var success = function (position) {
                        latLng = new google.maps.LatLng(
                            position.coords.latitude,
                            position.coords.longitude
                        );
                        stores.maps.overview.updateLocation(latLng);
                        // Clear other form fields before submitting form
                        $('#id_query, #id_group').val('');
                        $('#store-search').submit();
                    };
                    navigator.geolocation.getCurrentPosition(success, error);
                } else {
                    oscar.messages.error('Your location could not be determined');
                }
            });
        },

        // Create the initial map
        createOverviewMap: function(markerLatLng) {
            var map = new google.maps.Map($('#store-map')[0], {
                // We don't set a centre as adding the stores will 
                // centre the map.
                center: new google.maps.LatLng(0, 0),
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: false,
                zoomControl: true,
                scrollwheel: true,
                zoom: 17
            });
            var bounds = new google.maps.LatLngBounds();

            if (markerLatLng) {
                var marker = new google.maps.Marker({
                    position: markerLatLng,
                    map: map,
                    title: 'You are here',
                    visible: true,
                    icon: 'http://www.google.com/mapfiles/arrow.png'
                });
                bounds.extend(markerLatLng);
                map.fitBounds(bounds);

                var infowindow = new google.maps.InfoWindow({
                    content: 'You are here'
                });
                google.maps.event.addListener(marker, "click", function () {
                    infowindow.open(map, marker);
                });
            }

            google.maps.event.addDomListener(
                window, 'load', stores.maps.overview.addStoreMarkers(map, bounds));
            return map;
        },

        addStoreMarkers: function (map, bounds) {
            $('address').each(function(elem) {
                var storeLatLng = new google.maps.LatLng(
                    $(this).data('lat'),
                    $(this).data('lng')
                );
                bounds.extend(storeLatLng);

                var storeMarker = new google.maps.Marker({
                    position: storeLatLng,
                    map: map,
                    title: $(this).data('name'),
                    visible: true
                });
                map.fitBounds(bounds);

                var infowindow = new google.maps.InfoWindow({
                    content: this.innerHTML
                });

                // Open the infowindow on marker click
                google.maps.event.addListener(storeMarker, "click", function () {
                    infowindow.open(map, storeMarker);
                });
            });
        },

        // Persist a LatLng in the hidden input
        updateLocation: function(latLng) {
            $('#id_latitude').val(latLng.lat());
            $('#id_longitude').val(latLng.lng());
        }
    },

    // Return current LatLng
    getCurrentLatLng: function () {
        var latitude = $('#id_latitude').val(),
            longitude = $('#id_longitude').val();
        if (latitude && longitude) {
            return new google.maps.LatLng(
                parseFloat(latitude),
                parseFloat(longitude)
            );
        }
        return null;
    },

    // Return a JSON representation of a latLng that can be serialised
    // for storage in a hidden input.
    getGeoJsonFromLatLng: function (latLng) {
        return {
            'type': 'Point',
            // The GeoJSON format provides latitude and longitude
            // in reverse order in the 'coordinates' list:
            // [x, y] => [longitude, latitude]
            'coordinates': [latLng.lng(), latLng.lat()]
        };
    },

    // Return a LatLng object from a JSON string
    getLatLngFromGeoJSON: function (data) {
        // The GeoJSON format provides latitude and longitude
        // in reverse order in the 'coordinates' list:
        // [x, y] => [longitude, latitude]
        var point = $.parseJSON(data);
        return new google.maps.LatLng(
            point.coordinates[1],
            point.coordinates[0]
        );
    },

    createIndividualMap: function (mapElem, addressElem, zoomLevel) {
        lat = addressElem.data('lat');
        lng = addressElem.data('lng');

        if (lat & lng) {
            storeLatLng = new google.maps.LatLng(lat, lng);

            map = new google.maps.Map(mapElem, {
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: true,
                scrollwheel: false,
                zoom: zoomLevel
            });

            marker = new google.maps.Marker({
                position: storeLatLng,
                map: map
            });

            map.setCenter(storeLatLng);

            if (!zoomLevel) {
                bounds = new google.maps.LatLngBounds();
                bounds.extend(storeLatLng);
                map.fitBounds(bounds);
                map.setCenter(bounds.getCenter());
            }

            return {
                map: map,
                location: storeLatLng
            };
        }
    }
};
