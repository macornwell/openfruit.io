root = exports ? this
root.openfruit = root.openfruit ? {}
root.openfruit.geography = root.openfruit.geography ? {}

class GeoUtilities

  textCoordinateToGMapsDict:(stringCoordinate)->
    result = stringCoordinate.split(' ');
    return {lat:parseFloat(result[0]), lng: parseFloat(result[1])};

root.openfruit.geography.GeoUtilities = GeoUtilities
