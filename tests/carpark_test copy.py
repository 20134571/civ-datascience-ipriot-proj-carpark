import unittest
import sys,os
cwd = os.path.dirname(__file__)
sys.path.append(os.path.dirname(cwd) + "/smartpark") # simulating that the file is sititng alongside

#Change the line below to import your manager class
from mocks import MockCarparkManager

class TestConfigParsing(unittest.TestCase):
    
    def test_(self):
        # arrange - put together data for test
        carpark = MockCarparkManager()
        #act
        # assert 
        #self.assertTrue(True)   # will always say it has 1000 spaces
        self.assertEqual(1000, carpark.available_spaces)   # will always say it has 1000 spaces

if __name__=="__main__":
    unittest.main()
    print (cwd)
