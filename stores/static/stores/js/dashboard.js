var stores = stores || {};

stores.dashboard = {
    defaultLng: -37.82850537866209,
    defaultLat: 144.9661415816081,

    getLatLngFromGeoJSON: function (data) {
        var point = null;
        try {
            point = jQuery.parseJSON(data);
        } catch (e) {}

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
        var locationJSON = jQuery('#id_location').val(),
        latLng;

        if (locationJSON) {
            latLng = stores.dashboard.getLatLngFromGeoJSON(locationJSON);
        } else {
            latLng = null;
        }

        var input = jQuery('#search-text-field'),
        autocomplete = new google.maps.places.Autocomplete(input[0]),
        zoom = 17,
        marker = null;

        stores.dashboard.map = new google.maps.Map(document.getElementById('store-map'), {
            zoom: zoom,
            center: latLng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        marker = new google.maps.Marker({
            position: latLng,
            map: stores.dashboard.map,
            draggable: true,
            visible: true,
            icon: 'http://www.google.com/mapfiles/arrow.png'
        });

        stores.dashboard.geocoder = new google.maps.Geocoder();
        stores.dashboard.autocomplete_serv = new google.maps.places.AutocompleteService();

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

        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            var place = autocomplete.getPlace();
            if(!place.geometry) {
                return;
            }
            stores.dashboard.updateMarkerPlace(marker, place);
        });

        input.keypress(function(e) {
            if(e.which == 13) { // 13 is for Enter key
                e.preventDefault();
                stores.dashboard.updateToBestMatch(input, marker);
            }
        });

        stores.dashboard.openingHoursForm();
    },

    updateToBestMatch: function(input, marker) {
        var query = input.val();
        if(!query) {
            return;
        }
        stores.dashboard.autocomplete_serv.getQueryPredictions(
            {'input': query},
            function(results, status) {
                if(status === google.maps.places.PlacesServiceStatus.OK) {
                    var address = results[0].description;
                    input.trigger('blur');
                    input.val(address);
                    stores.dashboard.updateToAddress(address, marker);
                    input.trigger('change');
                }
            }
            );
    },

    updateMarkerPlace: function(marker, place) {
        if (place.geometry.viewport) {
            stores.dashboard.map.fitBounds(place.geometry.viewport);
        } else {
            stores.dashboard.map.setCenter(place.geometry.location);
            stores.dashboard.map.setZoom(17);  // Why 17? Because it looks good.
        }

        marker.setPosition(place.geometry.location);
        stores.dashboard.updateMarkerPosition(place.geometry.location);
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
                alert(gettext("did not receive valid geo position"));
            }
        });
    },

    updateToAddress: function(address, marker) {
        stores.dashboard.geocoder.geocode(
            {'address': address},
            function(results, status){
                if(status == google.maps.GeocoderStatus.OK) {
                    var latLang = results[0].geometry.location;
                    stores.dashboard.updateMarkerPlace(marker, results[0]);
                }
            }
            );
    },

    openingHoursForm: function(){
        function isOpenCallback() {
            var isopen = $(this).prop('checked');
            var inputs = $(this).closest('.weekday-block').find('input[type=text],button');
            inputs.prop('disabled', !isopen);
        }
        $('#opening_hours_form input[name$=open]').each(isOpenCallback)
                                                   .click(isOpenCallback);

        $('#opening_hours_form button.add-more').click(function(e){
            e.preventDefault();
            $(this).closest('.weekday-block').find('.hour-input.hide').first().removeClass('hide');
            return false;
        });
    }
};


$(document).ready(function() {
    // Adds error icon if there are erros in the product form
    $('[data-behaviour="affix-nav-errors"].tab-pane').each(function (){
        var productErrorListener = $(this).find('[class*="error"]').closest('.tab-pane').attr('id');
        $('[data-spy="affix"] a[href="#' + productErrorListener + '"]').append('<i class="icon-exclamation-sign pull-right"></i>');
    });
});
