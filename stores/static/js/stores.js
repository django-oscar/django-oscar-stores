var stores = stores || {};

stores.maps = {
    createOverviewMap: function () {
        $('.store-map').each(function (elem) {
            var myOptions = {
                center: new google.maps.LatLng(-37.813988, 144.964256),
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: false,
                zoomControl: true,
                scrollwheel: true,
                zoom: 11
            };
            var map = new google.maps.Map(this, myOptions);
            var bounds = new google.maps.LatLngBounds();

            $('address').each(function (elem) {
                var storeLocation = new google.maps.LatLng(
                    $(this).attr('data-lat'),
                    $(this).attr('data-lng')
                );
                bounds.extend(storeLocation);

                var marker = new google.maps.Marker({
                    position: storeLocation,
                    map: map,
                    title: $(this).attr('data-name')
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
    },
    createIndividualMap: function (mapElem, addressElem, zoomLevel) {
        lat = addressElem.attr('data-lat');
        lng = addressElem.attr('data-lng');

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

stores.dashboard = {
    init: function () {
        var latInit = document.getElementById('id_latitude').value,
            lngInit = document.getElementById('id_longitude').value,
            input = document.getElementById('searchTextField'),
            autocomplete = new google.maps.places.Autocomplete(input),
            zoom = 17,
            latLng = new google.maps.LatLng(latInit, lngInit),
            marker = null;

        if (!latInit & !lngInit) {
            latInit = -37.8136111;
            lngInit = 144.9630555;
            zoom = 10;

            latLng = new google.maps.LatLng(latInit, lngInit);
            stores.dashboard.updateMarkerPosition(latLng);
        }

        stores.dashboard.geocoder = new google.maps.Geocoder();

        stores.dashboard.map = new google.maps.Map(document.getElementById('storeMap'), {
            zoom: zoom,
            center: latLng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        marker = new google.maps.Marker({
            position: latLng,
            title: 'Image Location',
            map: stores.dashboard.map,
            draggable: true
        });

        stores.dashboard.geocodePosition(latLng);

        google.maps.event.addListener(marker, 'drag', function () {
            stores.dashboard.updateMarkerPosition(marker.getPosition());
        });

        google.maps.event.addListener(marker, 'dragend', function () {
            stores.dashboard.geocodePosition(marker.getPosition());
        });

        var update_timeout = null;
        google.maps.event.addListener(stores.dashboard.map, 'click', function (event) {
            update_timeout = setTimeout(function () {
                marker.setPosition(event.latLng);
                stores.dashboard.updateMarkerPosition(event.latLng);
            }, 200);
        });

        google.maps.event.addListener(stores.dashboard.map, 'dblclick', function (event) {
            if (update_timeout !== null) {
                clearTimeout(update_timeout);
            }
        });

        google.maps.event.addListener(autocomplete, 'enter', function () {
            var place = autocomplete.getPlace();
            if (place.geometry.viewport) {
                stores.dashboard.map.fitBounds(place.geometry.viewport);
            } else {
                stores.dashboard.map.setCenter(place.geometry.location);
                stores.dashboard.map.setZoom(17);  // Why 17? Because it looks good.
            }

            marker.setPosition(place.geometry.location);
            stores.dashboard.updateMarkerPosition(place.geometry.location);
        });

        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            var place = autocomplete.getPlace();
            if (place.geometry.viewport) {
                stores.dashboard.map.fitBounds(place.geometry.viewport);
            } else {
                stores.dashboard.map.setCenter(place.geometry.location);
                stores.dashboard.map.setZoom(17);  // Why 17? Because it looks good.
            }

            marker.setPosition(place.geometry.location);
            stores.dashboard.updateMarkerPosition(place.geometry.location);
        });
    },
    updateMarkerPosition: function (latLng) {
        document.getElementById('id_latitude').value = latLng.lat();
        document.getElementById('id_longitude').value = latLng.lng();
    },
    geocodePosition: function (pos) {
        stores.dashboard.geocoder.geocode({
            latLng: pos
        }, function (responses) {
            if (!responses || responses.length < 0) {
                alert("did not receive valid geo position");
            }
        });
    }
};
