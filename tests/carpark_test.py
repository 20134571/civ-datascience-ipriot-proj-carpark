import unittest
import sys,os
cwd = os.path.dirname(__file__)
sys.path.append(os.path.dirname(cwd))

#Change the line below to import your manager class
from smartpark.mocks import MockCarparkManager

class TestConfigParsing(unittest.TestCase):
    
    def test_(self):
        # arrange
        # act
        # assert
        self.assertTrue(True)

if __name__=="__main__":
    unittest.main()
