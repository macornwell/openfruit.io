// Generated by CoffeeScript 1.12.7
(function() {
  var TaxonomyDAL, ref, ref1, root,
    bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.openfruit = (ref = root.openfruit) != null ? ref : {};

  root.openfruit.taxonomy = (ref1 = root.openfruit.taxonomy) != null ? ref1 : {};

  TaxonomyDAL = (function() {
    var __fruitingPlants, __fruitingPlantsNotPublicURL, __moveFruitingPlantURL;

    __fruitingPlantsNotPublicURL = 'api/v1/plants/public';

    __moveFruitingPlantURL = '/api/v1/plants/move';

    __fruitingPlants = '/api/v1/fruiting-plants/';

    function TaxonomyDAL(easyData) {
      this.movedFruitingObject = bind(this.movedFruitingObject, this);
      this.getBoundingBoxOfFruit = bind(this.getBoundingBoxOfFruit, this);
      this.getPublicFruitingPlants = bind(this.getPublicFruitingPlants, this);
      this.getSpecies = bind(this.getSpecies, this);
      this._easyData = easyData;
    }

    TaxonomyDAL.prototype.getSpecies = function(speciesId, callback) {
      return this._easyData.getSingleObject('species', speciesId, callback);
    };

    TaxonomyDAL.prototype.getPublicFruitingPlants = function(callback, includeUsers, species) {
      var queryParams;
      if (includeUsers == null) {
        includeUsers = false;
      }
      if (species == null) {
        species = null;
      }
      queryParams = '?';
      if (!includeUsers) {
        queryParams += 'no-user&';
      }
      if (species) {
        queryParams += 'species=' + species + '&';
      }
      return this._easyData.getManyResults(__fruitingPlantsNotPublicURL + queryParams, callback);
    };

    TaxonomyDAL.prototype.getBoundingBoxOfFruit = function(callback, north_east, south_west) {
      var queryParams;
      queryParams = '?';
      queryParams += 'north_east=' + north_east + '&south_west=' + south_west;
      return this._easyData.getManyResults(__fruitingPlants + queryParams, callback);
    };

    TaxonomyDAL.prototype.movedFruitingObject = function(fruitingPlantID, newCoordinate, successCallback, errorCallback) {
      var data;
      if (successCallback == null) {
        successCallback = null;
      }
      if (errorCallback == null) {
        errorCallback = null;
      }
      data = {
        'fruiting_plant_id': fruitingPlantID,
        'coordinate': newCoordinate
      };
      return this._easyData.post(__moveFruitingPlantURL, data, successCallback, errorCallback);
    };

    return TaxonomyDAL;

  })();

  root.openfruit.taxonomy.TaxonomyService = TaxonomyDAL;

}).call(this);

//# sourceMappingURL=taxonomy-service.js.map
