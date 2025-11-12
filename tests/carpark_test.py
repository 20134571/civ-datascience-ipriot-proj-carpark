import unittest
import sys,os
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
        self.assertEqual(135, carpark.available_spaces)   # will always say it has 1001 spaces

    def test_car_in(self):
        #arrange
        carpark = MockCarparkManager()
        #assert
        carpark.incoming_car("LICENCE")
        #act
        self.assertEqual(134,carpark.available_spaces)
        self.assertEqual(0,carpark._total_cars_in)

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
        #act
        carpark.outgoing_car("LICENCE")
        #assert
        self.assertEqual(135,carpark.available_spaces)   #should increase a spot 

if __name__=="__main__":
    unittest.main()
    print (cwd + Parent )