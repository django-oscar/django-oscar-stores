var stores = stores || {};

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
            chocolatebox.dashboard.stores.updateMarkerPosition(latLng);
        }

        chocolatebox.dashboard.stores.geocoder = new google.maps.Geocoder();

        chocolatebox.dashboard.stores.map = new google.maps.Map(document.getElementById('storeMap'), {
            zoom: zoom,
            center: latLng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        marker = new google.maps.Marker({
            position: latLng,
            title: 'Image Location',
            map: chocolatebox.dashboard.stores.map,
            draggable: true
        });

        chocolatebox.dashboard.stores.geocodePosition(latLng);

        google.maps.event.addListener(marker, 'drag', function () {
            chocolatebox.dashboard.stores.updateMarkerPosition(marker.getPosition());
        });

        google.maps.event.addListener(marker, 'dragend', function () {
            chocolatebox.dashboard.stores.geocodePosition(marker.getPosition());
        });

        var update_timeout = null;
        google.maps.event.addListener(chocolatebox.dashboard.stores.map, 'click', function (event) {
            update_timeout = setTimeout(function () {
                marker.setPosition(event.latLng);
                chocolatebox.dashboard.stores.updateMarkerPosition(event.latLng);
            }, 200);
        });

        google.maps.event.addListener(chocolatebox.dashboard.stores.map, 'dblclick', function (event) {
            if (update_timeout !== null) {
                clearTimeout(update_timeout);
            }
        });

        google.maps.event.addListener(autocomplete, 'enter', function () {
            var place = autocomplete.getPlace();
            if (place.geometry.viewport) {
                chocolatebox.dashboard.stores.map.fitBounds(place.geometry.viewport);
            } else {
                chocolatebox.dashboard.stores.map.setCenter(place.geometry.location);
                chocolatebox.dashboard.stores.map.setZoom(17);  // Why 17? Because it looks good.
            }

            marker.setPosition(place.geometry.location);
            chocolatebox.dashboard.stores.updateMarkerPosition(place.geometry.location);
        });

        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            var place = autocomplete.getPlace();
            if (place.geometry.viewport) {
                chocolatebox.dashboard.stores.map.fitBounds(place.geometry.viewport);
            } else {
                chocolatebox.dashboard.stores.map.setCenter(place.geometry.location);
                chocolatebox.dashboard.stores.map.setZoom(17);  // Why 17? Because it looks good.
            }

            marker.setPosition(place.geometry.location);
            chocolatebox.dashboard.stores.updateMarkerPosition(place.geometry.location);
        });
    },
    updateMarkerPosition: function (latLng) {
        document.getElementById('id_latitude').value = latLng.lat();
        document.getElementById('id_longitude').value = latLng.lng();
    },
    geocodePosition: function (pos) {
        chocolatebox.dashboard.stores.geocoder.geocode({
            latLng: pos
        }, function (responses) {
            if (!responses || responses.length < 0) {
                alert("did not receive valid geo position");
            }
        });
    }
};
