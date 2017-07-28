root = exports ? this
root.openfruit = root.openfruit ? {}
root.openfruit.geography = root.openfruit.geography ? {}


class GeographyService
  __publicLocationsURL = '/api/v1/location/'

  constructor:(easyData)->
    @_easyData = easyData

  get_public_locations:(callback)=>
    return @_easyData.getManyResults(__publicLocationsURL, callback)

root.openfruit.geography.GeographyService = GeographyService