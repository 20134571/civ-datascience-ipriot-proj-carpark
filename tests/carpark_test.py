import unittest
import sys,os
import time
from datetime import datetime
import logging
from pathlib import Path
cwd = Path(os.path.dirname(__file__))
parent = str (cwd.parent)
#sys.path.append(os.path.dirname(cwd)+ "/smartpark") # simulating that the file is sititng alongside)

sys.path.append(parent +"/smartpark") # simulating that the file is sititng alongside)

#Change the line below to import your manager class
from mocks import MockCarparkManager

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
        carpark.log_record(car)  # write to log
        #assert
        self.assertEqual(134,carpark.available_spaces)
        #self.assertEqual(0,carpark._total_cars_in)

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
        carpark.incoming_car("LICENCE")
        self.assertEqual(134,carpark.available_spaces)
        time.sleep(61)  #wait a minute to ensure time difference for duration calculation
        #act
        carpark.outgoing_car("LICENCE")
        #assert
        self.assertEqual(135,carpark.available_spaces)   #should increase a spot 

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

    def test_incoming_car_logging(self):
        "tests that a car log entry is generated correctly when a car enters"
        #arrange
        carpark = MockCarparkManager()
        with self.assertLogs(level='INFO') as log_capture:
            #act
            carpark.incoming_car(Test_123)
            #assert
            self.assertEqual(len(log_capture.output), 1, "Expected exactly one log record.")

            log_message = log_capture.output[0]

            # 3. Check for the fixed, critical content: license plate and status 'In'
            self.assertIn(f"'license_plate': '{Test_123}'", log_message, 
                    "The logged message should contain the correct license plate.")
            self.assertIn(f"'status': 'In'", log_message,
                    "The logged message should show the car status as 'In'.")

if __name__=="__main__":
    unittest.main()
    print (cwd + Parent )