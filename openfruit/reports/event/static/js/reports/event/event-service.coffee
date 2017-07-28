root = exports ? this
root.openfruit = root.openfruit ? {}
root.openfruit.reports = root.openfruit.reports ? {}
root.openfruit.reports.event = root.openfruit.reports.event ? {}


class EventService
  __getEventsUrl = 'api/v1/reports/event/'
  __addEventURL = 'api/v1/reports/event/add/'

  constructor:(easyData)->
    @_easyData = easyData

  createEventRecord:(recordType, fruitingPlantID, successCallback, errorCallback)=>
    data = {
      'event_type':recordType,
      'fruiting_plant_id': fruitingPlantID
    }
    @_easyData.post(__addEventURL, data, successCallback, errorCallback)

  getEvents:(successCallback, errorCallback, fruitingPlantID=null, submittedBy=null, eventType=null, types=[])=>
    data = {
      'fruiting_plant_id': fruitingPlantID,
      'submitted_by': submittedBy,
      'event_type': eventType,
      'types': types,
    }
    @_easyData.getManyResultsWithData(__getEventsUrl, data, successCallback)


root.openfruit.reports.event.EventService = EventService