from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config
import time
import logging
import os

if __name__=="__main__":
    carpark = MockCarparkManager()
    self._spaces = int(configuration["total-spaces"])
    print(self._spaces)