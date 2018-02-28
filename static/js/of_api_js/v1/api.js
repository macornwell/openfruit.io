// Generated by CoffeeScript 1.9.3
(function() {
  var FruitSearchQuery, OpenFruitAPI, ref, root,
    bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.openfruit = (ref = root.openfruit) != null ? ref : {};

  FruitSearchQuery = (function() {
    function FruitSearchQuery(species, states, uses, year_low, year_high, ripening_low, ripening_high, references, chromosomes, resistances) {
      this.species = species != null ? species : null;
      this.states = states != null ? states : [];
      this.uses = uses != null ? uses : [];
      this.year_low = year_low != null ? year_low : null;
      this.year_high = year_high != null ? year_high : null;
      this.ripening_low = ripening_low != null ? ripening_low : null;
      this.ripening_high = ripening_high != null ? ripening_high : null;
      this.references = references != null ? references : [];
      this.chromosomes = chromosomes != null ? chromosomes : null;
      this.resistances = resistances != null ? resistances : [];
    }

    return FruitSearchQuery;

  })();

  OpenFruitAPI = (function() {
    OpenFruitAPI.__url_prefix = 'http://www.openfruit.io/api/v1';

    OpenFruitAPI.__token_url = '/auth/token/';

    function OpenFruitAPI(username, password) {
      this.username = username;
      this.password = password;
      this.get_states_with_cultivars = bind(this.get_states_with_cultivars, this);
      this.get_disease_types = bind(this.get_disease_types, this);
      this.get_authors = bind(this.get_authors, this);
      this.get_references = bind(this.get_references, this);
      this.search_fruiting_plants = bind(this.search_fruiting_plants, this);
      this.search_species = bind(this.search_species, this);
      this.fruit_search = bind(this.fruit_search, this);
      this.get_chromosomes = bind(this.get_chromosomes, this);
      this.get_ripenings = bind(this.get_ripenings, this);
      this.get_species_with_cultivars = bind(this.get_species_with_cultivars, this);
      this.get_species = bind(this.get_species, this);
      this.__build_query_string = bind(this.__build_query_string, this);
      this.__query = bind(this.__query, this);
      this.__get_token = bind(this.__get_token, this);
      this.__setup_ajax_post = bind(this.__setup_ajax_post, this);
      this.__build_query = bind(this.__build_query, this);
    }

    OpenFruitAPI.prototype.__build_query = function(url, key_value_dict) {
      var i, key, len, value;
      for (value = i = 0, len = key_value_dict.length; i < len; value = ++i) {
        key = key_value_dict[value];
        if (value === !null) {
          url += key + '=' + value + '&';
        }
      }
      return url;
    };

    OpenFruitAPI.prototype.__setup_ajax_post = function() {
      var csrftoken;
      csrftoken = Cookies.get('csrftoken');
      return $.ajaxSetup({
        beforeSend: (function(_this) {
          return function(xhr, settings) {
            return xhr.setRequestHeader("X-CSRFToken", csrftoken);
          };
        })(this)
      });
    };

    OpenFruitAPI.prototype.__get_token = function(callback) {
      var data, token_url;
      this.__setup_ajax_post();
      token_url = OpenFruitAPI.__url_prefix + OpenFruitAPI.__token_url;
      data = {
        url: token_url,
        data: JSON.stringify({
          username: this.username,
          password: this.password
        }),
        contentType: "application/json",
        type: 'POST',
        success: (function(_this) {
          return function(data) {
            var token;
            token = 'JWT ' + data['token'];
            return callback(token);
          };
        })(this),
        error: (function(_this) {
          return function(something) {
            return console.log(something);
          };
        })(this)
      };
      return $.ajax(data);
    };

    OpenFruitAPI.prototype.__query = function(callback, url) {
      return this.__get_token((function(_this) {
        return function(token) {
          return $.ajax({
            url: url,
            data: {},
            type: 'GET',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Authorization': token
            },
            success: function(data) {
              return callback(data);
            },
            error: function(error) {
              return console.log(error);
            }
          });
        };
      })(this));
    };

    OpenFruitAPI.prototype.__build_query_string = function(key_value_dict, split_value) {
      var i, key, len, query, v, value, value_string;
      if (split_value == null) {
        split_value = '&';
      }
      query = '';
      for (key in key_value_dict) {
        value = key_value_dict[key];
        if (!value) {
          continue;
        }
        if (value instanceof Array) {
          value_string = '';
          for (i = 0, len = value.length; i < len; i++) {
            v = value[i];
            value_string += v + ',';
          }
          value = value_string;
        }
        if (value) {
          query += key + '=' + value + split_value;
        }
      }
      return query;
    };


    /*
    Taxonomy API
     */

    OpenFruitAPI.prototype.get_species = function(callback, species_id) {
      var data, url;
      if (species_id == null) {
        species_id = null;
      }

      /*
      {
      "count": 55,
      "next": "http://openfruit.io/api/v1/states-with-cultivars/?limit=20&offset=20",
      "previous": "http://openfruit.io/api/v1/states-with-cultivars/?limit=20",
      "results": [
          {
              "state_id": 217,
              "country": "http://openfruit.io/api/v1/country/924/",
              "name": "Michigan",
              "abbreviation": "MI",
              "geocoordinate": "http://openfruit.io/api/v1/geocoordinate/79452/",
              "generated_name": "Michigan, US",
              "url": "http://openfruit.io/api/v1/state/217/"
          },
      }
       */
      url = OpenFruitAPI.__url_prefix + 'species/?';
      data = {
        'species_id': species_id
      };
      url = this.__build_query(url, data);
      return this.__query(callback, url);
    };

    OpenFruitAPI.prototype.get_species_with_cultivars = function(callback) {
      var url;
      url = OpenFruitAPI.__url_prefix + 'species_list/?cultivars__is_null=False';
      return this.__query(callback, url);
    };

    OpenFruitAPI.prototype.get_ripenings = function(callback) {
      var url;
      url = OpenFruitAPI.__url_prefix + 'ripenings/';
      return this.__query(callback, url);
    };

    OpenFruitAPI.prototype.get_chromosomes = function(callback) {
      var url;
      url = OpenFruitAPI.__url_prefix + 'chromosomes/';
      return this.__query(callback, url);
    };

    OpenFruitAPI.prototype.fruit_search = function(callback, query_or_query_list) {
      var data, i, len, q, url;
      url = OpenFruitAPI.__url_prefix + '/fruit-search/?';
      if (!query_or_query_list instanceof Array) {
        query_or_query_list = [query_or_query_list];
      }
      for (i = 0, len = query_or_query_list.length; i < len; i++) {
        q = query_or_query_list[i];
        url += 'query=';
        data = {
          'species': q.species,
          'states': q.states,
          'uses': q.uses,
          'year_low': q.year_low,
          'year_high': q.year_high,
          'ripening_low': q.ripening_low,
          'ripening_high': q.ripening_high,
          'references': q.references,
          'chromosomes': q.chromosomes,
          'resistances': q.resistances
        };
        url += this.__build_query_string(data, '$');
      }
      return this.__query(callback, url);
    };

    OpenFruitAPI.prototype.search_species = function(callback) {
      return '';
    };

    OpenFruitAPI.prototype.search_fruiting_plants = function(callback) {
      return '';
    };


    /*
    Fruit References API
     */

    OpenFruitAPI.prototype.get_references = function(callback, type, author) {
      var data, url;
      if (type == null) {
        type = null;
      }
      if (author == null) {
        author = null;
      }
      url = OpenFruitAPI.__url_prefix + 'fruit-references/';
      data = {
        'type': type,
        'author': author
      };
      url = this.__build_query(url);
      return this.__query(callback, url);
    };

    OpenFruitAPI.prototype.get_authors = function(callback) {
      var url;
      url = OpenFruitAPI.__url_prefix + 'authors/';
      return this.__query(callback, url);
    };


    /*
    Disease API
     */

    OpenFruitAPI.prototype.get_disease_types = function(callback) {
      var url;
      url = OpenFruitAPI.__url_prefix + 'disease-types/';
      return this.__query(callback, url);
    };


    /*
    Geography API
     */

    OpenFruitAPI.prototype.get_states_with_cultivars = function(callback) {
      var url;
      url = OpenFruitAPI.__url_prefix + 'states-with-cultivars/';
      return this.__query(callback, url);
    };

    return OpenFruitAPI;

  })();

  root.openfruit.OpenFruitAPI = OpenFruitAPI;

  root.openfruit.FruitSearchQuery = FruitSearchQuery;

}).call(this);

//# sourceMappingURL=api.js.map
