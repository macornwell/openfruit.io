root = exports ? this
root.openfruit = root.openfruit ? {}

class EasyRestData
  __genericURL = '/api/v1/{0}/'

  constructor:(cache=true, url=null)->
    @shouldCache = cache
    @_urlToObjs = {}
    if url
      __genericURL = url

  clearCache:()=>
    @_urlToObjs = {}

  getManyResults: (url, callback) =>
    objs = []
    if @shouldCache
      objs = @_urlToObjs[url]
    if objs
      callback(objs)
      return
    objs = []
    $.get(url, (data)=>
      _.each(data, (obj)->
        objs.push(obj)
      )
      if @shouldCache
        @_urlToObjs[url] = objs
      callback(objs)
    )

  getManyResultsWithData: (url, toSendData, callback) =>
    objs = []
    $.get(url, toSendData, (data)=>
      _.each(data['results'], (obj)->
        objs.push(obj)
      )
      callback(objs)
    )

  getSingle: (url, callback)=>
    obj = null
    if @shouldCache
      obj = @_urlToObjs[url]
    if obj
      callback(obj)
      return
    $.get(url, (obj)=>
      if @shouldCache
        @_urlToObjs[url] = obj
      callback(obj)
    )

  getSingleObject:(restObjName, id, callback)=>
    url = @getObjectURL(restObjName) + id
    @getSingle(url, callback)

  getManyObjectsWithForeignKey:(restObjName, foreignKeyName, foreignObjID, callback)=>
    url = @getObjectURL(restObjName) + '?' + foreignKeyName + '_id=' + foreignObjID
    @getManyResults(url, callback)


  getObjectURL:(restObjName)=>
    return __genericURL.format(restObjName)

  post:(url, data, successCallback, errorCallback) =>
    setup_ajax_post()
    $.ajax({
      url: url
      type: 'POST',
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify(data),
      dataType: 'text',
      success: successCallback,
      error: errorCallback
    });

setup_ajax_post = ()=>
  csrftoken = Cookies.get('csrftoken')
  $.ajaxSetup({
    beforeSend: (xhr, settings) => xhr.setRequestHeader("X-CSRFToken", csrftoken)
  })

root.openfruit.setup_ajax_post = setup_ajax_post
root.openfruit.EasyRestData = EasyRestData
