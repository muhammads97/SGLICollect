#
# Copyright (c) 2024 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#

from pathlib import Path
from src.extractors.extractor_interface import Extractor
from src.extractors.jasmes_extractor import JASMESExtractor
import numpy as np
from netCDF4 import Dataset

class JASMESMultiExtractor(Extractor):
    def __init__(self, paths: dict):
        self.__paths = paths

    def get_pixel(self, lat:float, lon:float) -> dict:
        for path in self.__paths:
            prod_str = 