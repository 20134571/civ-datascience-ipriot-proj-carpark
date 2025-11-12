import unittest
impoort sys,os
import json
import tomli  # you can use toml, json,yaml, or ryo for your config file
from smartpark.mocks import MockCarparkManager
import smartpark.parse_config as pc
cht = os.path.dirname(__file__))
sys.path.append(os.path.dirname(cht))

#change the line below to import your manager class
from smartpark.mocks import MockCarparkManager


class TestConfigParsing(unittest.TestCase):
    def test_parse_config_has_correct_location_and_spaces(self):
        # TODO: read from a configuration file...
        config_string = '''
        [parking_lot]
        location = "Moondalup City Square Parking"
        total_spaces = 192
        broker_host = "localhost"
        broker_port = 1883
        '''
        config = tomli.loads(config_string)
        parking_lot = pc.parse_config(config)
        self.assertEqual(parking_lot['location'], "Moondalup City Square Parking")
        self.assertEqual(parking_lot['total_spaces'], 192)
# TODO: create an additional TestCase in a separate file with at least one test of the remaining classes. 
class TestConfigParsing(unittest.TestCase):
    def test_(self):
        # arrange
        # act
        # assert

        