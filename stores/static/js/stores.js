var stores = stores || {};

stores.maps = {

    overview: {
        defaultLng: -37.82850537866209,
        defaultLat: 144.9661415816081,

        init: function () {
            var latLng = stores.maps.getCurrentLatLng();
            var map = stores.maps.createOverviewMap(latLng);


            // init autocomplete
            var input = $('#id_store_search'),
                autocomplete = new google.maps.places.Autocomplete(input[0]);

            google.maps.event.addListener(autocomplete, 'place_changed', function () {
                var place = autocomplete.getPlace();

                // update hidden field
                $('#id_location').val(JSON.stringify(stores.maps.getGeoJsonFromLatLng(place.geometry.location)));
                setTimeout(function () {
                    $('#store-search').submit();
                }, 500);
            });

            google.maps.event.addListener(autocomplete, 'enter', function () {
                var place = autocomplete.getPlace();

                // update hidden field
                $('#id_location').val(JSON.stringify(stores.maps.getGeoJsonFromLatLng(place.geometry.location)));
                setTimeout(function () {
                    $('#store-search').submit();
                }, 500);
            });


            // callback function for when coordinates are found
            $('[data-behaviours~=geo-location]').live('click', function(ev) {
                ev.preventDefault();

                // get location from browser
                if (navigator.geolocation) {
                    // callback function for when location could not be determined
                    var error = function(msg) {
                        oscar.messages.error(msg);
                    };

                    var success = function (position) {
                        latLng = new google.maps.LatLng(
                            position.coords.latitude,
                            position.coords.longitude
                        );
                        // populate hidden field
                        $('#id_location').val(JSON.stringify(stores.maps.getGeoJsonFromLatLng(latLng)));

                        // submit form
                        $('#store-search').submit();

                    };
                    navigator.geolocation.getCurrentPosition(success, error);
                } else {
                    oscar.messages.error('Your location could not be determined');
                }
            });

            $('[data-behaviours~=filter-group]').on('change', function() {
                $('#store-search').submit();
            });

        },

        addStoreMarkers: function (map, bounds) {

            $('address').each(function (elem) {
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

        }
    },

    getCurrentLatLng: function () {
        var latLng = null;
        if (!!$('#id_location').val()) {
            latLng = stores.maps.getLatLngFromGeoJSON($('#id_location').val());
        }
        return latLng;
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

    createOverviewMap: function (latLng) {
        var map = new google.maps.Map($('#store-map')[0], {
            center: new google.maps.LatLng(
                stores.maps.overview.defaultLat,
                stores.maps.overview.defaultLng
            ),
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            disableDefaultUI: false,
            zoomControl: true,
            scrollwheel: true,
            zoom: 17
        });


        var bounds = new google.maps.LatLngBounds();



        if (!!latLng) {
            setTimeout(function () {
                var marker = new google.maps.Marker({
                    position: latLng,
                    map: map,
                    title: 'You are here',
                    visible: true,
                    icon: 'http://www.google.com/mapfiles/arrow.png'
                });
                bounds.extend(latLng);
                map.fitBounds(bounds);
                map.setZoom(11);
                map.setCenter(latLng);

                var infowindow = new google.maps.InfoWindow({
                    content: 'You are here'
                });
                google.maps.event.addListener(marker, "click", function () {
                    infowindow.open(map, marker);
                });

            }, 500);
        }

        google.maps.event.addDomListener(window, 'load', stores.maps.overview.addStoreMarkers(map, bounds));

        return map;
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
