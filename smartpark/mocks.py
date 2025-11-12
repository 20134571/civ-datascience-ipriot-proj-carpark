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
    - The manager class should provide information to potential customers:
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
        self._total_spaces = self.configuration ["total_spaces"]
        self.unuseable_spaces = self.configuration.get("unuseable_spaces",0)
        self._available_spaces = self._total_spaces - self.unuseable_spaces

        #set log_file file path
        log_filename = self.configuration.get ("log_file", "")
        self.log_file = os.path.join(self.LOGGING, log_filename)
        #self._spaces = int(self.configuration["total-spaces"])
        self.cars_log = []
        self._total_cars_in = len(self.cars_log)
        
        # configure logging once
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',  # optional timestamp
            datefmt='%H:%M:%S'
        )

    @property
    def _total_cars_in(self):
        return 1
        #return int(self._available_spaces)
    
    @property
    def available_spaces(self):
        return int(self._available_spaces - self._total_cars) #1000
        #return int(self._available_spaces)

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
        self._total_cars += 1
        event_time= time.strftime("%H:%M:%S")
        license = Car(license_plate)
        self.cars_log.append({"license": license, "time": event_time, "event": "In"})
        print('Car in! ' + license_plate)

        #self._cars.append(Car(licence_plate)):

    def outgoing_car(self,license_plate):
        event_time= time.strftime("%H:%M:%S")
        license = Car(license_plate)
        for car in self.cars_log
            if car["license"] == license_plate and car["event"] == "In":
                car_found = car
                time_in = car["time"]
                break
        if car_found:
            self.cars_log.remove(car_found)           #if new licence plate is in list, Car.car_info(self.license_plate), then remove from list
            self._total_cars += -1

        else:
            exit_log = {"license": license_plate, "time_in": time_in, "time": event_time, "event": "Out"}
            # no put this into a log
        print('Car out! ' + license_plate)
        #for car in self._cars:
        #    car_found

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
                 
if __name__ == '__main__':
    print(_spaces)
    