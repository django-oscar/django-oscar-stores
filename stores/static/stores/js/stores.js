var stores = (function(s, gmaps, o) {
    s.maps = {
        'overview': {
            init: function(marker) {
                var map = s.maps.overview.createOverviewMap(marker);
                s.maps.overview.initAutocomplete();
                s.maps.overview.initGeoLocation();

                // Submit form when a user selects a store type
                $('[data-behaviours~=filter-group]').on('change', function () {
                    $('#store-search').submit();
                });
            },

            initAutocomplete: function() {
                var input = $('#id_query'),
                    autocomplete = new gmaps.places.Autocomplete(input[0]);

                // 'placed_changed' event fires when a user selects a place from the
                // autocomplete predictions.  We update the hidden location input with
                // a geo-json version of the LatLng and submit the form after a short delay.
                gmaps.event.addListener(autocomplete, 'place_changed', function() {
                    var place = autocomplete.getPlace();
                    if (place.geometry) {
                        s.maps.overview.updateLocation(place.geometry.location);
                        $('#store-search').submit();
                    }
                });
            },

            initGeoLocation: function() {
                $('[data-behaviours~=geo-location]').live('click', function (ev) {
                    if (navigator.geolocation) {
                        // Define callbacks for error/success
                        var error = o.messages.error;
                        var success = function (position) {
                            latLng = new gmaps.LatLng(
                                position.coords.latitude,
                                position.coords.longitude
                            );
                            s.maps.overview.updateLocation(latLng);
                            // Clear other form fields before submitting form
                            $('#id_query, #id_group').val('');
                            $('#store-search').submit();
                        };
                        navigator.geolocation.getCurrentPosition(success, error);
                    } else {
                        o.messages.error('Your location could not be determined');
                    }
                });
            },

            // Create the initial map
            createOverviewMap: function(markerLatLng) {
                var map = new gmaps.Map($('#store-map')[0], {
                    // We don't set a centre as adding the stores will 
                    // centre the map.
                    center: new gmaps.LatLng(0, 0),
                    mapTypeId: gmaps.MapTypeId.ROADMAP,
                    disableDefaultUI: false,
                    zoomControl: true,
                    scrollwheel: true,
                    zoom: 17
                });
                var bounds = new gmaps.LatLngBounds();

                if (markerLatLng) {
                    var marker = new gmaps.Marker({
                        position: markerLatLng,
                        map: map,
                        visible: true,
                        icon: 'http://www.google.com/mapfiles/arrow.png'
                    });
                    bounds.extend(markerLatLng);
                    map.fitBounds(bounds);
                }

                gmaps.event.addDomListener(
                    window, 'load', s.maps.overview.addStoreMarkers(map, bounds));
                return map;
            },

            addStoreMarkers: function (map, bounds) {
                $('address').each(function(elem) {
                    var storeLatLng = new gmaps.LatLng(
                        $(this).data('lat'),
                        $(this).data('lng')
                    );
                    bounds.extend(storeLatLng);

                    var storeMarker = new gmaps.Marker({
                        position: storeLatLng,
                        map: map,
                        title: $(this).data('name'),
                        visible: true
                    });
                    map.fitBounds(bounds);

                    var infowindow = new gmaps.InfoWindow({
                        content: this.innerHTML
                    });

                    // Open the infowindow on marker click
                    gmaps.event.addListener(storeMarker, "click", function () {
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

        initStore: function() {
            $('.store-map').each(function(elem) {
                s.maps.createIndividualMap(this, $('.store-details address'), 16);
                $(this).css({width: $(this).parents('.row-fluid').width()});
            });
        },

        createIndividualMap: function (mapElem, addressElem, zoomLevel) {
            lat = addressElem.data('lat');
            lng = addressElem.data('lng');

            if (lat & lng) {
                storeLatLng = new gmaps.LatLng(lat, lng);

                map = new gmaps.Map(mapElem, {
                    mapTypeId: gmaps.MapTypeId.ROADMAP,
                    disableDefaultUI: true,
                    scrollwheel: false,
                    zoom: zoomLevel
                });
                map.setCenter(storeLatLng);

                marker = new gmaps.Marker({
                    position: storeLatLng,
                    map: map
                });

                if (!zoomLevel) {
                    bounds = new gmaps.LatLngBounds();
                    bounds.extend(storeLatLng);
                    map.fitBounds(bounds);
                    map.setCenter(bounds.getCenter());
                }
            }
        }
    };
    return s;

})(stores || {}, google.maps, oscar);
