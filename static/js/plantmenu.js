// Generated by CoffeeScript 1.10.0
(function() {
  var PlantMenuFactory, cultivarHTML, endPreviousRecord, menuHTML, no_record, previousRecords, record, ref, root, startPreviousRecord,
    bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.openfruit = (ref = root.openfruit) != null ? ref : {};

  menuHTML = "<div>\n    <h3>{0}</h3><i class=\"fa fa-info\" aria-hidden=\"true\"></i>\n</div>";

  cultivarHTML = "<div>\n  <div class=\"button-group\">\n    <a data-toggle=\"modal\" data-record-id=\"{0}\" data-event-type=\"Leafing Out\" data-plant=\"{1}\" data-target=\"#confirm\" class=\" btn btn-default btn-lg\" href=\"#\">\n      <i class=\"fa fa-leaf\" aria-hidden=\"true\"></i></a>\n    <a data-toggle=\"modal\" data-record-id=\"{0}\" data-event-type=\"Blooming\" data-plant=\"{1}\" data-target=\"#confirm\" class=\"unicode-icon btn btn-default btn-lg\" href=\"#\">\n        <span>&#x273F</span></a>\n    <a data-toggle=\"modal\" data-record-id=\"{0}\" data-event-type=\"Ripening\" data-plant=\"{1}\" data-target=\"#confirm\" class=\"btn btn-default btn-lg\" href=\"#\">\n        <i class=\"fa fa-apple\" aria-hidden=\"true\"></i></a>\n    <a data-toggle=\"modal\" data-record-id=\"{0}\" data-event-type=\"Died\" data-plant=\"{1}\" data-target=\"#confirm\" class=\"btn btn-default btn-lg\" href=\"#\">\n        <i class=\"fa fa-times\" aria-hidden=\"true\"></i></a>\n  </div>\n  <h3 class=\"cultivar-name\">{1}<a href=\"#\"<i class=\"fa fa-info info-link\" aria-hidden=\"true\"></i></a></h3>\n  <span class=\"species-name\">Species: {2}</span>\n  <br>\n  <span>Managed By:{3}</span>\n";

  previousRecords = "<div>\n  <ul>\n    <li>Last Leafing Out Record: {0} ({1} total)</li>\n    <li>Last Bloom Record: {2} ({3} total)</li>\n    <li>Last Ripening Record: {4} ({5} total)</li>\n  </ul>\n</div>";

  startPreviousRecord = "<div>\n<ul>";

  endPreviousRecord = "</ul>\n</div>";

  record = "<li><strong>Last {0}:</strong> {1} ({2} total)</li>";

  no_record = "<li>No {0} Records Yet</li>";

  PlantMenuFactory = (function() {
    var __eventUrl;

    __eventUrl = '';

    function PlantMenuFactory() {
      this._countMatches = bind(this._countMatches, this);
      this._get_latest_event_by_datetime = bind(this._get_latest_event_by_datetime, this);
      this._create_record = bind(this._create_record, this);
      this.createEventSummary = bind(this.createEventSummary, this);
      this.createAddMenu = bind(this.createAddMenu, this);
      this.createMenuForCultivar = bind(this.createMenuForCultivar, this);
      this.createMenu = bind(this.createMenu, this);
    }

    PlantMenuFactory.prototype.createMenu = function(fruitingPlant) {
      var result;
      if (fruitingPlant.cultivar) {
        return this.createMenuForCultivar(fruitingPlant);
      } else {
        result = menuHTML.format(fruitingPlant.species_name);
      }
      return result;
    };

    PlantMenuFactory.prototype.createMenuForCultivar = function(fruitingPlant) {
      var result;
      result = cultivarHTML.format(fruitingPlant.fruiting_plant_id, fruitingPlant.cultivar_name, fruitingPlant.species_name, fruitingPlant.manager_username);
      return result;
    };

    PlantMenuFactory.prototype.createAddMenu = function() {
      return '';
    };

    PlantMenuFactory.prototype.createEventSummary = function(events) {
      var j, len, text, type, types;
      text = startPreviousRecord;
      types = ['Leafing Out', 'Blooming', 'Ripening'];
      for (j = 0, len = types.length; j < len; j++) {
        type = types[j];
        text += this._create_record(events, type);
        text += '\n';
      }
      text += endPreviousRecord;
      return text;
    };

    PlantMenuFactory.prototype._create_record = function(events, type) {
      var count, latest, text;
      count = this._countMatches(events, (function(_this) {
        return function(plant) {
          return plant.event_type_text === type;
        };
      })(this));
      if (count === 0) {
        return no_record.format(type);
      } else {
        latest = this._get_latest_event_by_datetime(events, type);
        text = latest.datetime;
        return record.format(type, text, count);
      }
    };

    PlantMenuFactory.prototype._get_latest_event_by_datetime = function(events, type) {
      var event, j, latest, len;
      latest = null;
      for (j = 0, len = events.length; j < len; j++) {
        event = events[j];
        if (event.event_type_text === type) {
          if (latest === null) {
            latest = event;
            break;
          }
        }
      }
      return latest;
    };

    PlantMenuFactory.prototype._countMatches = function(array, func) {
      var count, i;
      i = 0;
      count = 0;
      while (i < array.length) {
        if (func(array[i])) {
          console.log('match');
          count += 1;
        }
        i += 1;
      }
      return count;
    };

    return PlantMenuFactory;

  })();

  root.openfruit.PlantMenuFactory = PlantMenuFactory;

}).call(this);

//# sourceMappingURL=plantmenu.js.map
