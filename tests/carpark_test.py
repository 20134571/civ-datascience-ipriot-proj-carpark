import unittest
from unittest.mock import patch
import sys,os
import time
from datetime import datetime,timedelta
import logging
from pathlib import Path
cwd = Path(os.path.dirname(__file__))
parent = str (cwd.parent)
#sys.path.append(os.path.dirname(cwd)+ "/smartpark") # simulating that the file is sititng alongside)

sys.path.append(parent +"/smartpark") # simulating that the file is sititng alongside)

#Change the line below to import your manager class
from mocks import MockCarparkManager

# --- Mock Datetime Class for Test Control ---
class MockDatetime(datetime):
    """A class that mocks datetime.datetime.now() to return a fixed, 
    controllable time, or a time that can be advanced."""
    #set a predictable, initial time
    INITIAL_TIME = datetime(2025, 11, 20, 10, 30, 0)
    _test_time = INITIAL_TIME # internal rtacking variable
    
    @classmethod
    def now(cls, tz=None):
        """Returns the current controlled time."""
        return cls._test_time

    @classmethod
    def advance(cls, seconds):
        """Advances the internal test time."""
        cls._test_time += timedelta(seconds=seconds)

    @classmethod
    def reset(cls):
        """Resets the time to the initial value for a fresh test."""
        cls._test_time = cls.INITIAL_TIME
# ---------------------------------------------


class TestConfigParsing(unittest.TestCase):
     
    def test_fresh_carpark(self):
        # arrange - No data to arrange, checking setup of carpark from fresh
        #act
        carpark = MockCarparkManager()
        # assert 
        self.assertEqual(135, carpark.available_spaces)   # Pulling data from Queen Street configuration

    def test_car_in(self):
        #arrange
        carpark = MockCarparkManager()
        #act
        carpark.incoming_car("LICENCE")
        #carpark.log_record(car)  # write to log
        #assert
        self.assertEqual(134,carpark.available_spaces)
        #self.assertEqual(0,carpark._total_cars_in)

    def test_available_spaces_clamped_at_zero(self):
        # arrange
        carpark = MockCarparkManager()
        carpark._available_spaces = 3      # starting capacity
        carpark._total_cars_in = 0         # no cars yet

        # act - simulate 4 cars entering
        for _ in range(4):
            carpark._total_cars_in += 1

        # assert
        self.assertEqual(carpark.available_spaces_raw, -1)  # internal can go negative
        self.assertEqual(carpark.available_spaces, 0)       # public display clamps to 0
    

    def test_car_out_unrecognised_plate(self): 
        #arrange
        carpark = MockCarparkManager()
        #act
        carpark.outgoing_car("LICENCE")
        #assert
        self.assertEqual(135,carpark.available_spaces)#will not free up a space

    def test_car_out_recognised_plate(self): # Make sure there is a difference and behaviour checks correctly
        #arrange
        carpark = MockCarparkManager()
        LICENCE = "MOCK_TIME"
        carpark.incoming_car("LICENCE")
        self.assertEqual(134,carpark.available_spaces)
        #act - The manager thinks 61 seconds have passsed (relevant for duaration calculator)
        carpark.outgoing_car("LICENCE")
        #assert
        self.assertEqual(135,carpark.available_spaces)   #should increase a spot 
        

    # Patch the datetime module used by your production code (e.g., mocks.py)
    @patch('mocks.datetime', MockDatetime)
    def test_car_out_recognised_plate_with_15_minute_stay(self): # Make sure there is a difference and behaviour checks correctly
        #arrange
        carpark = MockCarparkManager()
        LICENCE = "MOCK_TIME"
        car_found = {'license_plate': 'LICENCE', 'time_in': '10:00:00', 'time_out': None, 'status': 'In', 'date_in': '2025-1-1', 'date_out': None}
        #set the initial 'entry' time by calling the incoming function
        MockDatetime._test_time =datetime(2025, 1, 1, 10, 0, 0) #resets time
        carpark.incoming_car("LICENCE")
        self.assertEqual(134,carpark.available_spaces)
        #time.sleep()  #wait a minute to ensure time difference for duration calculation
        #act
        MockDatetime.advance(seconds=900) 
        #act - The manager thinks 900 seconds have passsed (relevant for duaration calculator)
        carpark.outgoing_car("LICENCE")
        #assert
        self.assertEqual(135,carpark.available_spaces)   #should increase a spot 
        self.assertGreater(carpark.last_car_out.duration_minutes, 14, "Duration should be over 14 minutes")    

    def test_temperature_output(self): # Make sure there is a difference and behaviour checks correctly
        #arrange
        carpark = MockCarparkManager()
        #act Test with an integer reading (30)
        carpark.temperature_reading(30)
        #assert
        self.assertEqual(30,carpark.temperature,"should return the set int temperature.") 
        #act
        carpark.temperature_reading(-5)
        #assert
        self.assertEqual(-5,carpark.temperature,"should handle negative temperature.") 
        #act
        carpark.temperature_reading(30.8)
        #assert
        self.assertEqual(30,carpark.temperature,"should reduce decimal to an integer.") 

    @patch('mocks.datetime', MockDatetime)
    def test_incoming_car_logging(self):
        """
        Tests that a car log entry is generated correctly when a car enters, 
        using a mocked, predictable timestamp.
        """
        # arrange
        self.carpark = MockCarparkManager()
        MockDatetime._test_time =datetime(2025, 1, 1, 10, 30, 0) #resets time
        LICENSE_PLATE = "TEST_IN_123"
        MockDatetime.reset()
        # The expected timestamp format will depend on your logging config.
        # Assuming a format like 'YYYY-MM-DD HH:MM:SS'
        #EXPECTED_TIME_STRING = "2025-11-20 10:30:00" # Matches MockDatetime.INITIAL_TIME
        EXPECTED_TIME_STRING = "10:30:00" # Matches MockDatetime.INITIAL_TIME
        
       # We patch the 'datetime' object within the module where 'MockCarparkManager' 
        # is defined (assumed to be 'mocks.py')
        
        with self.assertLogs(level='INFO') as log_capture:
            # act
            self.carpark.incoming_car(LICENSE_PLATE)
            
            # assert 
            self.assertEqual(len(log_capture.output), 1, "Expected exactly one log record.")

            log_message = log_capture.output[0]

            # 1. Check for the fixed content: license plate and status 'In'
            self.assertIn(f"'license_plate': '{LICENSE_PLATE}'", log_message, 
                          "The logged message should contain the correct license plate.")
            self.assertIn(f"'status': 'In'", log_message,
                          "The logged message should show the car status as 'In'.")
            
            
            # 2. CHECK THE TIMESTAMP (Demonstrates the benefit of the mock)
            # This assertion ensures the mock is working and the log message includes the correct time.
            self.assertIn(EXPECTED_TIME_STRING, log_message,
                          "The logged message should contain the exact mocked entry time.")
            self.assertIn(EXPECTED_TIME_STRING, log_message,
                          "The logged message should contain the exact mocked entry time.")
             
            
    @patch('mocks.datetime', MockDatetime)         
    def test_outcoming_car_logging(self):
        """
        Tests that a car log exit is generated correctly when a car exits, 
        using a mocked, predictable timestamp.
        """
        # arrange
        self.carpark = MockCarparkManager()
        MockDatetime._test_time =datetime(2025, 1, 1, 10, 30, 0) #resets time
        LICENSE_PLATE = "TEST_IN_123"
        MockDatetime.reset()
        # The expected timestamp format will depend on your logging config.
        # Assuming the timestamp format 'YYYY-MM-DD HH:MM:SS'
        #EXPECTED_TIME_STRING = "2025-11-20 10:30:00" # Matches MockDatetime.INITIAL_TIME
        EXPECTED_ENTRYTIME_STRING = "10:30:00" # Matches MockDatetime.INITIAL_TIME
        EXPECTED_EXITTIME_STRING = "10:45:00" # Matches MockDatetime.INITIAL_TIME
        EXPECTED_ENTRYDATE_STRING = "2025-11-20" # Matches MockDatetime.INITIAL_DATE
        
       # We patch the 'datetime' object within the module where 'MockCarparkManager' 
        # is defined (assumed to be 'mocks.py')
        
        with self.assertLogs(level='INFO') as log_capture:
            # act 1 - captire entry log_capture[0]
            self.carpark.incoming_car(LICENSE_PLATE)
            #advance by 900 seconds to simulate a 15 minute stay
            MockDatetime.advance(seconds=900) 
            #act - The manager thinks 900 seconds have passsed (relevant for duaration calculator)
            # act 2- captire entry log_capture[1]
            self.carpark.outgoing_car(LICENSE_PLATE)
            
            # assert 
            self.assertEqual(len(log_capture.output), 2, "Expected exactly one log record.")

            log_message_1 = log_capture.output[0]
            log_message_2 = log_capture.output[1]

            # 1. Check for the fixed content: license plate and status 'In'
            self.assertIn(f"'license_plate': '{LICENSE_PLATE}'", log_message_1, 
                          "The logged message should contain the correct license plate.")
            self.assertIn(f"'status': 'In'", log_message_1,
                           "The logged message should show the car status as 'In'.")
            self.assertIn(f"'license_plate': '{LICENSE_PLATE}'", log_message_2, 
                          "The logged message should contain the correct license plate.")
            self.assertIn(f"'status': 'Out'", log_message_2,
                           "The logged message should show the car status as 'Out'.")
            
            # 2. CHECK THE TIMESTAMP AND DATESTAMP (Demonstrates the benefit of the mock)
            # This assertion ensures the mock is working and the log message includes the correct time.
            self.assertIn(f"'time_in': '{EXPECTED_ENTRYTIME_STRING}'", log_message_1,
                           "The logged message should contain the exact mocked entry time.")
            self.assertIn(f"'time_out': '{EXPECTED_EXITTIME_STRING}'", log_message_2,
                          "The logged message should contain the exact mocked entry time.")
            self.assertIn(f"'date_in': '{EXPECTED_ENTRYDATE_STRING}'", log_message_1,
                           "The logged message should contain the exact mocked entry time.")
            self.assertIn(f"'date_in': '{EXPECTED_ENTRYDATE_STRING}'", log_message_2,
                           "The logged message should contain the exact mocked entry time.")
            self.assertIn(f"'date_out': '{EXPECTED_ENTRYDATE_STRING}'", log_message_2,
                           "The logged message should contain the exact mocked entry time.")
            
if __name__=="__main__":

        
    print (cwd + Parent )