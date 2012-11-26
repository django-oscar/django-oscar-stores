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
