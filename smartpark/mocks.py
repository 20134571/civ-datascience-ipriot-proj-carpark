from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config
import time

'''
    TODO: 
    - make your own module, or rename this one. Yours won't be a mock-up, so "mocks" is a bad name here.
    - Read your configuration from a file. 
    - Write entries to a log file when something happens.
    - The "display" should update instantly when something happens
    - Make a "Car" class to contain information about cars:
        * License plate number. You can use this as an identifier
        * Entry time
        * Exit time
    - The manager class should record all activity. This includes:
        * Cars arriving
        * Cars departing
        * Temperature measurements.
    - The manager class should provide informtaion to potential customers:
        * The current time (optional)
        * The number of bays available
        * The current temperature
    
'''
class MockCarparkManager(CarparkSensorListener,CarparkDataProvider):
    #constant, for where to get the configuration data
    CONFIG_FILE = "samples_and_snippets\\config2.json"

    def __init__(self):
        self.configuration = parse_config(MockCarparkManager.CONFIG_FILE, "Queen Street")
        #configuration = parse_config(MockCarparkManager.CONFIG_FILE,"Queen Street")
        self._temperature = 30

    @property
    def available_spaces(self):
        return 1000

    @property
    def temperature(self):
        return int(self._temperature)

    @property
    def current_time(self):
        return time.localtime()

    def temperature_reading(self,reading):
        self._temperature = reading
        print(f'temperature is {reading}')
        if hasattr(self, "display") and self.display is not None:
        self.display.update_display()

    def incoming_car(self,license_plate):
        print('Car in! ' + license_plate)

    def outgoing_car(self,license_plate):
        print('Car out! ' + license_plate)


class Car:
    def __init__(self,plate=None):
        self.LicensePlate = plate

if __name__ == '__main__':
    print(manager.configuration)
    print(manager.configuration["location"])       