// Generated by CoffeeScript 1.10.0
(function() {
  var EasyRestData, ref, root, setup_ajax_post,
    bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.openfruit = (ref = root.openfruit) != null ? ref : {};

  EasyRestData = (function() {
    var __genericURL;

    __genericURL = '/api/v1/{0}/';

    function EasyRestData(cache, url) {
      if (cache == null) {
        cache = true;
      }
      if (url == null) {
        url = null;
      }
      this.post = bind(this.post, this);
      this.getObjectURL = bind(this.getObjectURL, this);
      this.getManyObjectsWithForeignKey = bind(this.getManyObjectsWithForeignKey, this);
      this.getSingleObject = bind(this.getSingleObject, this);
      this.getSingle = bind(this.getSingle, this);
      this.getManyResultsWithData = bind(this.getManyResultsWithData, this);
      this.getManyResults = bind(this.getManyResults, this);
      this.clearCache = bind(this.clearCache, this);
      this.shouldCache = cache;
      this._urlToObjs = {};
      if (url) {
        __genericURL = url;
      }
    }

    EasyRestData.prototype.clearCache = function() {
      return this._urlToObjs = {};
    };

    EasyRestData.prototype.getManyResults = function(url, callback) {
      var objs;
      objs = [];
      if (this.shouldCache) {
        objs = this._urlToObjs[url];
      }
      if (objs) {
        callback(objs);
        return;
      }
      objs = [];
      return $.get(url, (function(_this) {
        return function(data) {
          _.each(data, function(obj) {
            return objs.push(obj);
          });
          if (_this.shouldCache) {
            _this._urlToObjs[url] = objs;
          }
          return callback(objs);
        };
      })(this));
    };

    EasyRestData.prototype.getManyResultsWithData = function(url, toSendData, callback) {
      var objs;
      objs = [];
      return $.get(url, toSendData, (function(_this) {
        return function(data) {
          _.each(data, function(obj) {
            return objs.push(obj);
          });
          return callback(objs);
        };
      })(this));
    };

    EasyRestData.prototype.getSingle = function(url, callback) {
      var obj;
      obj = null;
      if (this.shouldCache) {
        obj = this._urlToObjs[url];
      }
      if (obj) {
        callback(obj);
        return;
      }
      return $.get(url, (function(_this) {
        return function(obj) {
          if (_this.shouldCache) {
            _this._urlToObjs[url] = obj;
          }
          return callback(obj);
        };
      })(this));
    };

    EasyRestData.prototype.getSingleObject = function(restObjName, id, callback) {
      var url;
      url = this.getObjectURL(restObjName) + id;
      return this.getSingle(url, callback);
    };

    EasyRestData.prototype.getManyObjectsWithForeignKey = function(restObjName, foreignKeyName, foreignObjID, callback) {
      var url;
      url = this.getObjectURL(restObjName) + '?' + foreignKeyName + '_id=' + foreignObjID;
      return this.getManyResults(url, callback);
    };

    EasyRestData.prototype.getObjectURL = function(restObjName) {
      return __genericURL.format(restObjName);
    };

    EasyRestData.prototype.post = function(url, data, successCallback, errorCallback) {
      setup_ajax_post();
      return $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        dataType: 'text',
        success: successCallback,
        error: errorCallback
      });
    };

    return EasyRestData;

  })();

  setup_ajax_post = (function(_this) {
    return function() {
      var csrftoken;
      csrftoken = Cookies.get('csrftoken');
      return $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          return xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      });
    };
  })(this);

  root.openfruit.setup_ajax_post = setup_ajax_post;

  root.openfruit.EasyRestData = EasyRestData;

}).call(this);

//# sourceMappingURL=easy_rest_data.js.map