root = exports ? this
root.openfruit = root.openfruit ? {}



menuHTML = """
<div>
    <h3>{0}</h3><i class="fa fa-info" aria-hidden="true"></i>
</div>
"""

cultivarHTML = """
<div>
  <div class="button-group">
    <a data-toggle="modal" data-record-id="{0}" data-event-type="Leafing Out" data-plant="{1}" data-target="#confirm" class=" btn btn-default btn-lg" href="#">
      <i class="fa fa-leaf" aria-hidden="true"></i></a>
    <a data-toggle="modal" data-record-id="{0}" data-event-type="Blooming" data-plant="{1}" data-target="#confirm" class="unicode-icon btn btn-default btn-lg" href="#">
        <span>&#x273F</span></a>
    <a data-toggle="modal" data-record-id="{0}" data-event-type="Ripening" data-plant="{1}" data-target="#confirm" class="btn btn-default btn-lg" href="#">
        <i class="fa fa-apple" aria-hidden="true"></i></a>
    <a data-toggle="modal" data-record-id="{0}" data-event-type="Died" data-plant="{1}" data-target="#confirm" class="btn btn-default btn-lg" href="#">
        <i class="fa fa-times" aria-hidden="true"></i></a>
  </div>
  <h3 class="cultivar-name">{1}<a href="/cultivar/{0}"<i class="fa fa-info info-link" aria-hidden="true"></i></a></h3>
  <span class="species-name">Species: {2}</span>
  <br>
  <span>Added By:{3}</span>

"""

previousRecords = """
<div>
  <ul>
    <li>Last Leafing Out Record: {0} ({1} total)</li>
    <li>Last Bloom Record: {2} ({3} total)</li>
    <li>Last Ripening Record: {4} ({5} total)</li>
  </ul>
</div>
"""

startPreviousRecord = """
<div>
<ul>
"""

endPreviousRecord = """
</ul>
</div>
"""

record = """
<li><strong>Last {0}:</strong> {1} ({2} total)</li>
"""

no_record = """
<li>No {0} Records Yet</li>
"""

see_all_records = """
<div><a href="/fruiting-plant/details/{0}">Details</a></div>
"""


class PlantMenuFactory
  __eventUrl = ''

  constructor: ->

  createMenu:(fruitingPlant)=>
    if fruitingPlant.cultivar
      return @createMenuForCultivar(fruitingPlant)
    else
      result = menuHTML.format(fruitingPlant.species_name)
    return result

  createMenuForCultivar:(fruitingPlant)=>
    result = cultivarHTML.format(fruitingPlant.fruiting_plant_id, fruitingPlant.cultivar_name, fruitingPlant.species_name, fruitingPlant.manager_username)
    return result

  createAddMenu:()=>
    ''

  createEventSummary:(events)=>
    text = startPreviousRecord
    types = ['Leafing Out', 'Blooming', 'Ripening']
    for type in types
      text += @_create_record(events, type)
      text += '\n'
    text += endPreviousRecord

    return text

  createDetailsLink:(fruitingPlant)=>
    return see_all_records.format(fruitingPlant.fruiting_plant_id)

  _create_record: (events, type)=>
    count = @_countMatches(events, (plant)=>
      return plant.event_type_text == type
    )
    if count == 0
      return no_record.format(type)
    else
      latest = @_get_latest_event_by_datetime(events, type)
      text = latest.datetime
      return record.format(type, text, count)

  _get_latest_event_by_datetime:(events, type)=>
    latest = null;
    for event in events
      if event.event_type_text == type
        if latest == null
          latest = event
          break
    return latest

  _countMatches:(array, func)=>
    i = 0
    count = 0
    while (i < array.length)
        if func(array[i])
          count += 1
        i += 1
    return count

root.openfruit.PlantMenuFactory = PlantMenuFactory