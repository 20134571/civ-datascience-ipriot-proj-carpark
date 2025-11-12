import unittest
import json  # you can use toml, json,yaml, or ryo for your config file
import sys,os
cwd = os.path.dirname(__file__)
sys.path.append(os.path.dirname(cwd))
import smartpark.config_parser as pc


class TestConfigParsing(unittest.TestCase):
    def test_parse_config_has_correct_location_and_spaces(self):
        # TODO: read from a configuration file...
        config_string = '''
{
    "CarParks": [
        {
            "name": "raf-park-international",
            "total-spaces": 130,
            "total-cars": 0,
            "location": "moondalup",
            "broker": "localhost",
            "port": 1883,
            "Sensors": [
                {
                    "name": "sensor1",
                    "type": "entry"
                },
                {
                    "name": "sensor2",
                    "type": "exit"
                }
            ],
            "Displays": [
                {
                    "name": "display1"
                }
            ]
        }
    ]
}
        '''
        config = json.loads(config_string)
        parking_lot = pc.parse_config(config)
        self.assertEqual(parking_lot['location'], "Moondalup City Square Parking")
        self.assertEqual(parking_lot['total_spaces'], 192)
# TODO: create an additional TestCase in a separate file with at least one test of the remaining classes. 

if __name__=="__main__":
    unittest.main()