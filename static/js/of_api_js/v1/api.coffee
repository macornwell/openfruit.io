root = exports ? this
root.openfruit = root.openfruit ? {}

class FruitSearchQuery

    constructor:(@species=null, @states=[], @uses=[], @year_low=null, @year_high=null,
      @ripening_low=null, @ripening_high=null, @references=[], @chromosomes=null, @resistances=[]) ->


class OpenFruitAPI
  @__url_prefix: 'http://www.openfruit.io/api/v1'
  @__token_url: '/auth/token/'

  constructor:(@username, @password) ->

  __build_query:(url, key_value_dict) =>
    for key, value in key_value_dict
      if value is not null
        url += key + '=' + value + '&'
    return url


  __setup_ajax_post: ()=>
    csrftoken = Cookies.get('csrftoken')
    $.ajaxSetup({
      beforeSend: (xhr, settings) => xhr.setRequestHeader("X-CSRFToken", csrftoken)
    })

  __get_token:(callback) =>
    @__setup_ajax_post()
    token_url = OpenFruitAPI.__url_prefix + OpenFruitAPI.__token_url
    data = {
      url: token_url,
      data: JSON.stringify({
        username: @username,
        password: @password
      }),
      contentType: "application/json",
      type: 'POST',
      success: (data) =>
        token = 'JWT ' + data['token']
        callback(token)
      error: (something) =>
        console.log(something)
    }
    $.ajax(data)

  __query:(callback, url) =>
    @__get_token( (token) =>
      $.ajax({
        url: url,
        data: {},
        type: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': token,
        },
        success: (data) =>
          callback(data)
        error: (error) =>
          console.log(error)
      })
    )


  __build_query_string: (key_value_dict, split_value='&')=>
      query = ''
      for key, value of key_value_dict
        if not value
          continue
        if value instanceof Array
            value_string = ''
            for v in value
                value_string += v + ','
            value = value_string
        if value
            query += key + '=' + value + split_value
      return query


  ###
  Taxonomy API

  ###
  get_species:(callback, species_id=null)=>
    ###
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
    ###
    url = OpenFruitAPI.__url_prefix + 'species/?'
    data = {
      'species_id': species_id
    }
    url = @__build_query(url, data)
    @__query(callback, url)

  get_species_with_cultivars:(callback)=>
    url = OpenFruitAPI.__url_prefix + 'species_list/?cultivars__is_null=False'
    @__query(callback, url)

  get_ripenings:(callback)=>
    url = OpenFruitAPI.__url_prefix + 'ripenings/'
    @__query(callback, url)

  get_chromosomes:(callback)=>
    url = OpenFruitAPI.__url_prefix + 'chromosomes/'
    @__query(callback, url)

  fruit_search:(callback, query_or_query_list)=>
    url = OpenFruitAPI.__url_prefix + '/fruit-search/?'

    if not query_or_query_list instanceof Array
      query_or_query_list = [query_or_query_list]

    for q in query_or_query_list
      url += 'query='
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
          'resistances': q.resistances,
      }
      url += @__build_query_string(data, '$')
    @__query(callback, url)

  search_species:(callback)=>
    ''

  search_fruiting_plants:(callback)=>
    ''

  ###
  Fruit References API

  ###
  get_references:(callback, type=null, author=null)=>
    url = OpenFruitAPI.__url_prefix + 'fruit-references/'
    data = {
      'type': type,
      'author': author,
    }
    url = @__build_query(url)
    @__query(callback, url)

  get_authors:(callback)=>
    url = OpenFruitAPI.__url_prefix + 'authors/'
    @__query(callback, url)



  ###
  Disease API

  ###

  get_disease_types:(callback)=>
    url = OpenFruitAPI.__url_prefix + 'disease-types/'
    @__query(callback, url)


  ###
  Geography API

  ###
  get_states_with_cultivars:(callback)=>
    url = OpenFruitAPI.__url_prefix + 'states-with-cultivars/'
    @__query(callback, url)



root.openfruit.OpenFruitAPI = OpenFruitAPI
root.openfruit.FruitSearchQuery = FruitSearchQuery
