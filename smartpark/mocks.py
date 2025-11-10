from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config
import time
import logging
import os
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
    LOGGING = "samples_and_snippets\\"

    def __init__(self):
        self.configuration = parse_config(MockCarparkManager.CONFIG_FILE, "Queen Street")
        #configuration = parse_config(MockCarparkManager.CONFIG_FILE,"Queen Street")
        self._temperature = 30
        self._available_spaces = 999
        #set log_file file path
        log_filename = self.configuration.get ("log_file", "")
        self.log_file = os.path.join(self.LOGGING, log_filename)

        # configure logging once
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',  # optional timestamp
            datefmt='%H:%M:%S'
        )

    @property
    def available_spaces(self):
        return int(self._available_spaces)

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

    #logging method
    def log_record(self,car):   
        logging.info(car.car_info())  #log a car entry/exit

    def license_entered(self):
        self.license_plate = plate
        plate = self.plate_var.get().strip()
        if plate:
            #create a car object
            car = mocks.Car(plate)
            car.enter()
            #send to the manager
            for listener in self.listeners:
                listener.log_record(car)

            self.license_var.set("")    

    def license_exited(self):
        plate = self.license_var.get().strip()
        if plate:
            #create a car object
            car = mocks.Car(plate)
            car.exit()
            #send to the manager
            for listener in self.listeners:
                listener.log_record(car)

            self.license_var.set("")

class Car:
    def __init__(self,plate=None):
        self.license_plate = plate
        self.time_in = None
        self.time_out = None
        self.status = "Out" # if it is not in it is out and In is iniated by the enter process

    def enter(self):
        self.time_in = time.strftime("%H:%M:%S" )
        self.status ="In"

    def exit(self):
        self.time_out = time.strftime("%H:%M:%S" )
        self.status ="Out"

    def car_info(self):
        return {"license_plate" : self.license_plate, "time in" : self.time_in, "time_out" : self.time_out, "status" : self.status}
                 
#if __name__ == '__main__':
#    print(manager.configuration)
#    print(manager.configuration["location"])       