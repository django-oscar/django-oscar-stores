var stores = stores || {};

stores.maps = {

    overview: {
        init: function() {
            var map = stores.maps.createOverviewMap();

            // callback function for when coordinates are found
            var success = function(position) {
                var currentLocation = new google.maps.LatLng(
                    position.coords.latitude,
                    position.coords.longitude
                );
                var bounds = map.getBounds();
                bounds.extend(currentLocation);
                map.fitBounds(bounds);

                var marker = new google.maps.Marker({
                    position: currentLocation,
                    map: map,
                    title: 'You are here'
                });
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
