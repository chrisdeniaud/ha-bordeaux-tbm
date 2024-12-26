import unittest
from unittest.mock import patch
from tbm_api import get_lines, get_stops_for_line, get_next_departures

class TestTBMApi(unittest.TestCase):

    @patch('requests.get')
    def test_get_lines(self, mock_get):
        mock_response = {
            'Siri': {
                'LinesDelivery': {
                    'AnnotatedLineRef': [
                        {'LineRef': 'L1', 'LineName': 'Line 1'},
                        {'LineRef': 'L2', 'LineName': 'Line 2'}
                    ]
                }
            }
        }
        mock_get.return_value.json.return_value = mock_response
        lines = get_lines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0]['LineRef'], 'L1')
        self.assertEqual(lines[1]['LineRef'], 'L2')

    @patch('requests.get')
    def test_get_stops_for_line(self, mock_get):
        mock_response = {
            'Siri': {
                'StopPointsDelivery': {
                    'AnnotatedStopPointRef': [
                        {
                            "StopPointRef": {
                                "value": "bordeaux:StopPoint:BP:8341:LOC"
                            },
                            "StopAreaRef": {
                                "value": "bordeaux:StopPoint:BP:TLESEC:LOC"
                            },
                            "StopName": {
                                "value": "Les Ecus",
                                "lang": "fr"
                            },
                            "Lines": [
                                {
                                    "value": "bordeaux:Line:62:LOC"
                                }
                            ],
                            "Location": {
                                "latitude": 44.868911,
                                "longitude": -0.608897
                            }
                        },
                        {
                            "StopPointRef": {
                                "value": "bordeaux:StopPoint:BP:9673:LOC"
                            },
                            "StopAreaRef": {
                                "value": "bordeaux:StopPoint:BP:BSCOJJ:LOC"
                            },
                            "StopName": {
                                "value": "Collège Jean Jaurès",
                                "lang": "fr"
                            },
                            "Lines": [
                                {
                                    "value": "bordeaux:Line:801:LOC"
                                },
                                {
                                    "value": "bordeaux:Line:802:LOC"
                                },
                                {
                                    "value": "bordeaux:Line:803:LOC"
                                }
                            ],
                            "Location": {
                                "latitude": 44.862959,
                                "longitude": -0.516677
                            }
                        },
                    ]
                }
            }
        }
        # mock_get.return_value.json.return_value = mock_response
        stops = get_stops_for_line()
        self.assertEqual(len(stops), 2)
        self.assertEqual(stops[0]['StopPointRef'], 'bordeaux:StopPoint:BP:8341:LOC')

    @patch('requests.get')
    def test_get_next_departures(self, mock_get):
        mock_response = {
            'Siri': {
                'ServiceDelivery': {
                    'StopMonitoringDelivery': [{
                        'MonitoredStopVisit': [
                            {
                                'MonitoredVehicleJourney': {
                                    'LineRef': {'value': 'L1'},
                                    'DirectionRef': {'value': '1'},
                                    'MonitoredCall': {
                                        'ExpectedDepartureTime': '2023-10-10T10:00:00Z'
                                    },
                                    'DestinationName': [{'value': 'Destination 1'}]
                                }
                            }
                        ]
                    }]
                }
            }
        }
        mock_get.return_value.json.return_value = mock_response
        departures = get_next_departures('S1', 'L1', '1', 1)
        self.assertEqual(len(departures), 1)
        self.assertEqual(departures[0]['destination'], 'Destination 1')

if __name__ == '__main__':
    unittest.main()
