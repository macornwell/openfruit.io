// Generated by CoffeeScript 1.9.3
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
      this.searchCultivars = bind(this.searchCultivars, this);
      this.searchSpecies = bind(this.searchSpecies, this);
      this._easyData = easyData;
    }

    TaxonomyDAL.prototype.searchSpecies = function(token, value, callback) {
      var url;
      $('body').css('cursor', "progress");
      token = 'JWT ' + token;
      url = '/api/v1/species_list/?limit=10&generated_name=' + value;
      return $.ajax({
        url: url,
        data: {},
        type: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': token
        },
        success: (function(_this) {
          return function(data, status) {
            var species_list, suggestion_key_to_obj;
            $('body').css('cursor', "default");
            species_list = data['results'];
            suggestion_key_to_obj = {};
            species_list = Object.keys(species_list).map(function(k) {
              var key, species;
              species = species_list[k];
              key = species['name'] + ' (' + species['latin_name'] + ')';
              suggestion_key_to_obj[key] = species;
              return key;
            });
            return callback(species_list, suggestion_key_to_obj);
          };
        })(this)
      });
    };

    TaxonomyDAL.prototype.searchCultivars = function(species, ripening_high, ripening_low, year_high, year_low, state, uses, books, chromosome, resistances, callback) {
      var url;
      url = '/api/v1/fruit-search/?query=';
      if (species) {
        url += 'species=' + species + '&';
      }
      if (ripening_high) {
        url += 'ripening_high=' + ripening_high + '&';
      }
      if (ripening_low) {
        url += 'ripening_low=' + ripening_low + '&';
      }
      if (year_high) {
        url += 'year_high=' + year_high + '&';
      }
      if (year_low) {
        url += 'year_low=' + year_low + '&';
      }
      if (state) {
        url += 'state=' + state + ',&';
      }
      if (uses) {
        url += 'uses=' + uses + '&';
      }
      if (books) {
        url += 'books=' + books + '&';
      }
      if (chromosome) {
        url += 'chromosomes=' + chromosome + '&';
      }
      if (resistances) {
        url += 'resistances=' + resistances + '&';
      }
      console.log(url);
      return this._easyData.getManyResults(url, callback);
    };

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
