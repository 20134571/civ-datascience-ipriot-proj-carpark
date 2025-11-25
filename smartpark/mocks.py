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
        ##COMPLETE
    
'''
class MockCarparkManager(CarparkSensorListener,CarparkDataProvider):
    ############################################################
    # Carpark Manager Class that records all activity including:
    # cars arriving
    # cars departing
    # temperature measurements
    # outputs:
    # curret time
    # number of bays available
    # current temperature 
    # handles edge cases 

    ############################################################

    import threading        # REQUIRED FOR NEW TIMER
    #constant, for where to get the configuration data
    CONFIG_FILE = "samples_and_snippets\\config2.json"
    LOGGING = "samples_and_snippets\\"  

    def __init__(self):
        self.configuration = parse_config(MockCarparkManager.CONFIG_FILE, "Queen Street")
        #Adding code for timer improvement - need a source of knowledge, using Gemin in the absence of this being available.
        # ... (initialization code remains the same)
        self._update_signal = None # New attribute to store the event
                
        self._temperature = 30
        self._total_spaces = self.configuration ["total_spaces"]
        self.unuseable_spaces = self.configuration.get("unuseable_spaces",0)
        self._available_spaces = self._total_spaces - self.unuseable_spaces
        
        log_filename = self.configuration.get ("log_file", "")
        self.log_file = os.path.join(self.LOGGING, log_filename)
        #self.cars_log = [{'license_plate': '1DKH682', 'time_in': '17:44:41', 'time_out': None, 'status': 'In', 'date_in': '2025-11-18', 'date_out': None}]
        self.cars_log = []
        self._total_cars_in = 0 #len(self.cars_log)

        # configure logging once
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',  # optional timestamp
            datefmt='%Y-%m-%d--%H:%M:%S'
        )

    @property
    def available_spaces_raw(self):
        """
        Returns the raw number of available spaces, which may be negative
        """
        return int(self._available_spaces - self._total_cars_in) 
    
    @property
    def available_spaces(self):       # never reduces below zero - Clamp to zero for display
        """
        Returns the available spaces, which is never negaitve
        """
        return max(0, int(self.available_spaces_raw))
    
    @property
    def temperature(self):
        """
        Returns the current temperature as input from the GUI
        """
        return int(self._temperature)

    @property
    def current_time(self):
        """
        Returns the current time
        """
        return time.localtime()
    
    # Added this methods to enable the new timer in no_pi check_updates to communicate with CarparkDisplay
    def set_update_signal(self, update_event):
            """
            method to enable the new timer in no_pi check_updates to communicate with CarparkDisplay
            """
            self._update_signal = update_event

    def signal_update(self):
            """
            Sets the event to notify the CarParkDisplay to refresh.
            """
            if self._update_signal:
                self._update_signal.set()

        #Ended of added code to modfy timer

    def temperature_reading(self,reading):
        """
        Captures the current temperature
        """
        self._temperature = reading
        print(f'temperature is {reading}')
        if hasattr(self, "display") and self.display is not None:
            self.signal_update()


    def incoming_car(self,license_plate):
        """
        After updating the car count with a new car entry, signal the display to update
        logs the car details to a text log on entry
        """
        license_plate = license_plate.upper()
        self._total_cars_in += 1
        self.signal_update()  
                
        print('Car in! ' + license_plate)
        car = Car(license_plate)
        car.enter()
        event_date=  time.strftime("%Y-%m-%d")
        event_time= time.strftime("%H:%M:%S")
        
        new_car_record = car.car_info()
        self.cars_log.append(new_car_record)
        self.log_record(car)  # write to log
        print(f"Entry {new_car_record['license_plate']} logged at {new_car_record['time_in']}")
        
    def outgoing_car(self,license_plate):
        """
        Updates the car count with a car exit if it has entered and signals the display to update
        Does not updates the car count with a car exit if it has not entered and does not signal the display to update
        logs the car exit details for both scenarios to a text log on exit
        """
        license_plate = license_plate.upper()
        
        event_time = time.strftime("%H:%M:%S")
        event_date=  time.strftime("%Y-%m-%d")
        
        car_found = None
        
        for record in self.cars_log:
            if record["license_plate"] == license_plate and record["status"] == "In":
                car_found = record
                
                break

        if car_found is not None:
            car = Car(license_plate)
            #car.exit()                     

            car.time_in = car_found["time_in"]
            car.date_in = car_found["date_in"]
                    
            # Define date/time formats used in Car.enter() and Car.exit()
            DATE_FORMAT = "%Y-%m-%d"
            TIME_FORMAT = "%H:%M:%S"
            
            # EXPLICITLY SET EXIT TIME using datetime.now() (Ensures we get Mocked time in tests)
            now_time = datetime.now() # Gets real time, or MOCKED time during unit tests
            car.time_out = now_time.strftime(TIME_FORMAT)
            car.date_out = now_time.strftime(DATE_FORMAT)

            try:
                # Combine date and time strings into full datetime objects
                #datetime_in_str = f"{car.date_in} {car.time_in}"
                #datetime_out_str = f"{car.date_out} {car.time_out}"
                datetime_in_str = f"{car_found["date_in"]} {car_found["time_in"]}"
                datetime_out_str = f"{car.date_out} {car.time_out}"
              
                # FIX: Using the Time Date order for the format string
                DATETIME_FORMAT = f"{TIME_FORMAT} {DATE_FORMAT}" # e.g. "%H:%M:%S %Y-%m-%d"

                datetime_in = datetime.strptime(datetime_in_str, f"{DATE_FORMAT} {TIME_FORMAT}")
                datetime_out = datetime.strptime(datetime_out_str, f"{DATE_FORMAT} {TIME_FORMAT}")

                # Calculate timedelta
                duration_td: timedelta = datetime_out - datetime_in
                
                # Convert duration to total minutes (rounded to nearest minute) and store it
                # The duration is stored in the Car object for logging
                car.duration_minutes = round(duration_td.total_seconds() / 60)
                
                print(f"DEBUG: Duration calculated: {car.duration_minutes} minutes")
                
            except Exception as e:
                print(f"Error calculating duration for {license_plate}: {e}")
        
            #exit_car_record = {"license_plate": license_plate, "time_in": car.time_in, "time_out" : event_time, "status": "Out", "date_in" : car.date_in, "date_out" : event_date}
            self.cars_log.remove(car_found)  # remove from list
            self._total_cars_in -= 1
            self.signal_update()  # After updating the car count, signal the display to update ****
            
            final_log_data = car.car_info()
            self.last_car_out = car
            print(f"DEBUG: Logging exit data -> {final_log_data}")

            self.log_record(car)  # write to log


        else:
            car = Car(license_plate)
            car.exit()
            
            car.time_in = "N/A" 
            car.date_in = "N/A"
        
            self.log_record(car) # write to log
                    
        print('Car out! ' + license_plate)

    #logging method
    def log_record(self,car):
        """
        Logging method for car entry and exit
        """  
        logging.info(car.car_info())  #log a car entry/exit

    def queen_street_log(mock): 
        """
        Logging test method for specific car park 
        """  
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
        """
        car entry test for specific car park 
        """ 
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
        """
        car exit test for specific car park 
        """ 
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
    ############################################################
    # Car Class
    # A "Car" class to contain information about cars:
    #   * License plate number. Used as an identifier
    #   * Entry time
    #   * Exit time
     ############################################################
    def __init__(self,plate=None):
        self.license_plate = plate
        self.time_in = None
        self.time_out = None
        self.date_in = None
        self.date_out = None
        self.duration_minutes = None    
        self.status = "Out" # if it is not in it is out and In is iniated by the enter process

    def enter(self):
        now = datetime.now()
        self.time_in = now.strftime("%H:%M:%S" )
        self.date_in = now.strftime("%Y-%m-%d")
        self.status ="In"

    def exit(self):
        now = datetime.now()
        self.time_out = now.strftime("%H:%M:%S" )
        self.date_out = now.strftime("%Y-%m-%d")
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