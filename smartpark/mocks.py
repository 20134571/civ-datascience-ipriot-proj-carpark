from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config
import time
from datetime import datetime
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
        self._total_spaces = self.configuration ["total_spaces"]
        self.unuseable_spaces = self.configuration.get("unuseable_spaces",0)
        self._available_spaces = self._total_spaces - self.unuseable_spaces
        #Self._available_spaces = 999
        #set log_file file path
        log_filename = self.configuration.get ("log_file", "")
        self.log_file = os.path.join(self.LOGGING, log_filename)
        self.cars_log = [{'license_plate': '1DKH682', 'time_in': '17:44:41', 'time_out': None, 'status': 'In', 'date_in': '2025-11-18', 'date_out': None}]
        self._total_cars_in = 0 #len(self.cars_log)

        # configure logging once
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',  # optional timestamp
            datefmt='%Y-%m-%d--%H:%M:%S'
        )
 
    @property
    def available_spaces(self):
        return int(self._available_spaces - self._total_cars_in) 
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
        license_plate = license_plate.upper()
        self._total_cars_in += 1
        print('Car in! ' + license_plate)
        car = Car(license_plate)
        car.enter()
        event_date=  time.strftime("%Y-%m-%d")
        event_time= time.strftime("%H:%M:%S")
        #license = Car(license_plate)
        #new_car_record = {"license_plate": license_plate, "time_in": event_time, "status": "In", "date_in" : event_date}
        new_car_record = car.car_info()
        self.cars_log.append(new_car_record)
        self.log_record(car)  # write to log
        print(f"Entry {new_car_record['license_plate']} logged at {new_car_record['time_in']}")
        #if self._update_event:
        #    self._update_event.set()
        

    def outgoing_car(self,license_plate):
        license_plate = license_plate.upper()
        
        event_time = time.strftime("%H:%M:%S")
        event_date=  time.strftime("%Y-%m-%d")
        #license = Car(license_plate)

        car_found = None
        #time_in = None
        #date_in = None  

        for record in self.cars_log:
            if record["license_plate"] == license_plate and record["status"] == "In":
                car_found = record
                #time_in = record.get("time_in",None)
                #date_in = record.get("date_in",None)
                #print(self.cars_log)
                break

        if car_found is not None:
            car = Car(license_plate)
            car.exit()
            
            car.time_in = car_found["time_in"]
            car.date_in = car_found["date_in"]

            exit_car_record = {"license_plate": license_plate, "time_in": car.time_in, "time_out" : event_time, "status": "Out", "date_in" : car.date_in, "date_out" : event_date}
            self.cars_log.remove(car_found)  #if new licence plate is in list, Car.car_info(self.license_plate), then remove from list
            self._total_cars_in -= 1

            final_log_data = car.car_info()
            print(f"DEBUG: Logging exit data -> {final_log_data}")

            #self.cars_log.append(exit_car_record) - this is wrong as it writes to the variable cars_log not the text log. 
            self.log_record(car)  # write to log
            #exit_log = {
            #    "license": license_plate,
            #    "time_in": time_in, 
            #    "time_out": event_time, 
            #    "event": "Out", 
            #    "date in" : date_in, 
            #    "date_out" : event_date
            #}             

        else:
            car = Car(license_plate)
            car.exit()
            
            car.time_in = "N/A" 
            car.date_in = "N/A"

            #car.time_in = "None"
            #car.time_out = event_time, 
            #car.status = "Out"
            #car.date_in = "None", 
            #car.date_out = event_date
            #self.cars_log.append({"license_plate": license, "time_in": "None", "time_out" : event_time, "status": "Out", "date_in" : "None", "date_out" : event_date})
            self.log_record(car) # write to log
        
        print('Car out! ' + license_plate)
        #if self._update_event:
        #    self._update_event.set()
        #self.log_record(Car(license_plate))  # write to log

    #logging method
    def log_record(self,car):   
        logging.info(car.car_info())  #log a car entry/exit

    def queen_street_log(mock): 
        # Create a car for testing
        car1 = mocks.Car("1DKH682")
        car1.enter()
        print("Car entered:", car1.car_info())
        mock.log_record(car1)  # write to log

        # Wait a few seconds to simulate time passing
        time.sleep(10)

        car1.exit()
        print("Car exited:", car1.car_info())
        mock.log_record(car1)  # write to log

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
        self.date_in = None
        self.date_out = None
        self.status = "Out" # if it is not in it is out and In is iniated by the enter process

    def enter(self):
        self.time_in = time.strftime("%H:%M:%S" )
        self.date_in = time.strftime("%Y-%m-%d")
        self.status ="In"

    def exit(self):
        self.time_out = time.strftime("%H:%M:%S" )
        self.date_out = time.strftime("%Y-%m-%d")
        self.status ="Out"

    def car_info(self):
        return {
            "license_plate" : self.license_plate, 
            "time_in" : self.time_in, 
            "time_out" : self.time_out, 
            "status" : self.status,
            "date_in" : self.date_in, 
            "date_out" : self.date_out
        }                 
#if __name__ == '__main__':
#    print(manager.configuration)
#    print(manager.configuration["location"])       