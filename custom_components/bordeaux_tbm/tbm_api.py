"""TBM API client."""
import requests
from datetime import datetime
from dateutil import tz
from const import BASE_URL, API_KEY

def get_lines():
    """Get available lines."""
    response = requests.get(f"{BASE_URL}lines-discovery.json?AccountKey={API_KEY}")
    data = response.json()
    return data['Siri']['LinesDelivery']['AnnotatedLineRef']

def get_stops_for_line():
    """Get stops for a specific line."""
    response = requests.get(f"{BASE_URL}stoppoints-discovery.json?AccountKey={API_KEY}")
    data = response.json()
    stops = data['Siri']['StopPointsDelivery']['AnnotatedStopPointRef']
    #return [stop for stop in stops if line_ref in stop['Lines'][0]['value']]
    return [stop for stop in stops if 1 == 1]

def get_next_departures(stop_ref, line_ref, direction_ref, num_predictions):
    """Get next departures for a stop."""
    response = requests.get(f"{BASE_URL}stop-monitoring.json?AccountKey={API_KEY}&MonitoringRef={stop_ref}")
    data = response.json()
    departures = data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
    
    line_departures = [d for d in departures if (
        d['MonitoredVehicleJourney']['LineRef']['value'] == line_ref and 
        d['MonitoredVehicleJourney']['DirectionRef']['value'] == direction_ref and 
        'ExpectedDepartureTime' in d['MonitoredVehicleJourney']['MonitoredCall']
    )]
    
    sorted_departures = sorted(line_departures, 
        key=lambda x: x['MonitoredVehicleJourney']['MonitoredCall']['ExpectedDepartureTime']
    )

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Paris')    
    now = datetime.now(to_zone)
    
    formatted_departures = []
    for departure in sorted_departures[:num_predictions]:
        expected_time = datetime.fromisoformat(
            departure['MonitoredVehicleJourney']['MonitoredCall']['ExpectedDepartureTime'].replace('Z', '+00:00')
        ).replace(tzinfo=from_zone).astimezone(to_zone)
        
        delay = int((expected_time - now).total_seconds() // 60)
        destination = departure['MonitoredVehicleJourney']['DestinationName'][0]['value']
        
        formatted_departures.append({
            'time': expected_time.strftime('%H:%M'),
            'delay': delay,
            'destination': destination
        })
    
    return formatted_departures