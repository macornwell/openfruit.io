root = exports ? this
root.openfruit = root.openfruit ? {}
root.openfruit.taxonomy = root.openfruit.taxonomy ? {}


class TaxonomyDAL
  __fruitingPlantsNotPublicURL = 'api/v1/plants/public'
  __moveFruitingPlantURL = '/api/v1/plants/move'
  __fruitingPlants = '/api/v1/fruiting-plants/'

  constructor:(easyData)->
    @_easyData = easyData

  searchSpecies:(token, value, callback)=>
    $('body').css('cursor', "progress");
    token = 'JWT ' + token;
    url = '/api/v1/species_list/?limit=10&generated_name=' + value;
    $.ajax({
      url: url,
      data: {},
      type: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': token,
      },
      success: (data, status) =>
        $('body').css('cursor', "default")
        species_list = data['results']
        suggestion_key_to_obj = {}
        species_list = Object.keys(species_list).map((k)=>
          species = species_list[k]
          key = species['name'] + ' (' + species['latin_name'] + ')'
          suggestion_key_to_obj[key] = species
          return key
        )
        callback(species_list, suggestion_key_to_obj)
    })

  searchCultivars: (species, ripening_high, ripening_low, year_high
                    year_low, state, uses, books, callback) =>
    url = '/api/v1/fruit-search/?'
    if species
      url += 'species=' + species + '&'
    if ripening_high
      url += 'ripening_high=' + ripening_high + '&'
    if ripening_low
      url += 'ripening_low=' + ripening_low + '&'
    if year_high
      url += 'year_high=' + year_high + '&'
    if year_low
      url += 'year_low=' + year_low + '&'
    if state
      url += 'state=' + state + '&'
    if uses
      url += 'uses=' + uses + '&'
    if books
      url += 'books=' + books + '&'
    @_easyData.getManyResults(url, callback)


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
