root = exports ? this
root.openfruit = root.openfruit ? {}
root.openfruit.taxonomy = root.openfruit.taxonomy ? {}


class TaxonomyDAL
  __fruitingPlantsNotPublicURL = 'api/v1/plants/public'
  __moveFruitingPlantURL = '/api/v1/plants/move'
  __fruitingPlants = '/api/v1/fruiting-plants/'

  constructor:(easyData)->
    @_easyData = easyData

  getSpecies:(speciesId, callback)=>
    return @_easyData.getSingleObject('species', speciesId, callback)

  getPublicFruitingPlants:(callback, includeUsers=false, species=null)=>
    queryParams = '?'
    if not includeUsers
      queryParams += 'no-user&'
    if species
      queryParams += 'species=' + species + '&'
    return @_easyData.getManyResults(__fruitingPlantsNotPublicURL + queryParams, callback)

  getBoundingBoxOfFruit:(callback, north_east, south_west)=>
    queryParams = '?'
    queryParams += 'north_east=' + north_east + '&south_west=' + south_west
    return @_easyData.getManyResults(__fruitingPlants + queryParams, callback)

  movedFruitingObject:(fruitingPlantID, newCoordinate, successCallback=null, errorCallback=null)=>
    data = {
      'fruiting_plant_id':fruitingPlantID,
      'coordinate': newCoordinate
    }
    @_easyData.post(__moveFruitingPlantURL, data, successCallback, errorCallback)




root.openfruit.taxonomy.TaxonomyService = TaxonomyDAL