var stores = stores || {};

stores.dashboard = {
    defaultLng: -37.82850537866209,
    defaultLat: 144.9661415816081,

    getLatLngFromGeoJSON: function (data) {
        var point = jQuery.parseJSON(data);

        if (!point || point.type.toLowerCase() !== "point") {
            return new google.maps.LatLng(
                stores.dashboard.defaultLng,
                stores.dashboard.defaultLat
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

    getGeoJsonFromLatLng: function (data) {
        return {
            'type': 'Point',
            // the GeoJSON format provides latitude and longitude
            // in reverse order in the 'coordinates' list:
            // [x, y] => [longitude, latitude]
            'coordinates': [data.lng(), data.lat()]
        };
    },

    init: function () {
        var locationInput = jQuery('#id_location');
        var latLng = stores.dashboard.getLatLngFromGeoJSON(locationInput.val());

        var input = jQuery('#search-text-field'),
            autocomplete = new google.maps.places.Autocomplete(input[0]),
            zoom = 17,
            marker = null;

        stores.dashboard.updateMarkerPosition(latLng);
        stores.dashboard.geocoder = new google.maps.Geocoder();

        stores.dashboard.map = new google.maps.Map(document.getElementById('store-map'), {
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
        var new_location = stores.dashboard.getGeoJsonFromLatLng(latLng);
        jQuery('#id_location').val(JSON.stringify(new_location));
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
