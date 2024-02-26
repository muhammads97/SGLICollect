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
from src.jasmes.jasmes_api import JASMESProd

'''
    NWLR_380            = "NWLR_380"
    NWLR_412            = "NWLR_412"
    NWLR_443            = "NWLR_443"
    NWLR_490            = "NWLR_490"
    NWLR_530            = "NWLR_530"
    NWLR_565            = "NWLR_565"
    NWLR_670            = "NWLR_670"
    CDOM                = "CDOM"
    CHLA                = "CHLA"
    TSM                 = "TSM"
    SST                 = "SST"
'''


class JASMESMultiExtractor(Extractor):
    def __init__(self, paths: dict):
        self.__paths = paths

    @classmethod
    def get_file_ext(self)->str:
        return "nc"
    @classmethod
    def make_file_name(self, path)->str:
        return path.split("/")[-1]

    def get_pixel(self, lat:float, lon:float) -> dict:
        result = {}
        for k in self.__paths.keys():
            prod = JASMESProd(k)
            extractor = JASMESExtractor(self.__paths[k], prod)
            pixel = extractor.get_pixel(lat, lon)
            result.update(pixel)
        return result

    @classmethod
    def extract_prod_name(self, key:str) -> str:
        return JASMESProd(key[9:])