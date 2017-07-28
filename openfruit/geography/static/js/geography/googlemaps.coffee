root = exports ? this
root.openfruit = root.openfruit ? {}
root.openfruit.geography = root.openfruit.geography ? {}

class LatLon

  constructor: (@lat, @lon)->

  getLatLon:()=>
    return { lat: @lat, lng: @lon}




class GoogleMaps
  constructor: (mapID, centerLatLon, zoom, shouldCluster=true)->
    @_shouldCluster = shouldCluster
    @_map = new google.maps.Map(document.getElementById(mapID), {
                zoom: zoom,
                mapTypeId: 'hybrid',
                center: centerLatLon,
                styles:
                  [
                    {
                      featureType: 'poi.business',
                      stylers: [{visibility: 'off'}]
                    },
                    {
                      featureType: 'transit',
                      elementType: 'labels.icon',
                      stylers: [{visibility: 'off'}]
                    }
                  ]
            })
    @_markers = []
    @_markerCluster = new MarkerClusterer(@_map, @_markers, {
      imagePath: 'https://cdn.rawgit.com/googlemaps/js-marker-clusterer/gh-pages/images/m',
      maxZoom: 18
    });
    setTimeout((=>google.maps.event.trigger(@_map, 'resize')), 1000);

  addMarker:(position, title, additionalDict={}, addToCluster=true)=>
    data = {
      position: position,
      map: @_map,
      title: title,
    }
    for key,value of additionalDict
      data[key] = value

    marker = new google.maps.Marker(data);
    @_markers.push(marker)
    if @_shouldCluster and addToCluster
      @_markerCluster.addMarker(marker, true);
    return marker


root.openfruit.geography.LatLon = LatLon
root.openfruit.geography.GoogleMaps = GoogleMaps




