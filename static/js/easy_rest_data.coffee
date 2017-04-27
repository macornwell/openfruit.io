root = exports ? this
root.grow_journal = root.grow_journal ? {}

class EasyRestData
  __genericURL = '/api/{0}/'

  constructor:(cache=true)->
    @shouldCache = cache
    @_urlToObjs = {}

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

setup_ajax_post = ()=>
  csrftoken = $.cookie('csrftoken')
  $.ajaxSetup({
    beforeSend: (xhr, settings) => xhr.setRequestHeader("X-CSRFToken", csrftoken)
  })

root.grow_journal.setup_ajax_post = setup_ajax_post
root.grow_journal.EasyRestData = EasyRestData
