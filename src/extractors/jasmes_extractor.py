#
# Copyright (c) 2023 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#

from pathlib import Path
from src.jasmes import JASMESInternalProd
from src.extractors.extractor_interface import Extractor
import numpy as np
from netCDF4 import Dataset

class JASMESExtractor(Extractor):
    def __init__(self, path: Path, prod:JASMESInternalProd):
        self.__prod = prod
        self.__nc = Dataset(path, "r")

    def __handle_digital_number(self, rrs:bool=False) -> np.ndarray[float, float]:
        """
        Convert digital number to the desired product

        :prod JASMESProd 
        """
        # Get data
        prod:str = str(self.__prod.value)

        data = self.__nc.variables[prod]
        # Convert DN to physical value
        if rrs:
            scale = data.Rrs_scale_factor
            offset = data.Rrs_add_offset
            digital_data = (data[:].data - data.add_offset)/data.scale_factor
            physical_data = digital_data * scale + offset
        else:
            physical_data = data[:].data
        physical_data[physical_data > data.Maximum_valid_DN] = np.nan
        physical_data[physical_data < data.Minimum_valid_DN] = np.nan
        return physical_data
    
    def get_lat_lon(self) -> tuple[list[float], list[float]]:
        return self.__nc.variables["Latitude"][:].data, self.__nc.variables["Longitude"][:].data
    
    @classmethod
    def get_file_ext(self)->str:
        return "nc"
    @classmethod
    def make_file_name(self, file_name)->str:
        return file_name

    def __find_entry(self, lat_arr, lon_arr, lat, lon) ->tuple[int, int]:
        dist = 1000
        lat_index = -1
        for i,l in enumerate(lat_arr):
            if np.abs(l - lat) < dist:
                dist = np.abs(l-lat)
                lat_index = i
        lon_index = -1
        dist = 1000
        for i,l in enumerate(lon_arr):
            if np.abs(l - lon) < dist:
                dist = np.abs(l-lon)
                lon_index = i
        return lat_index, lon_index

    def get_pixel(self, lat:float, lon:float) -> dict:
        lat_mat, lon_mat = self.get_lat_lon()
        row, col = self.__find_entry(lat_mat, lon_mat, lat, lon)
        if str(self.__prod.value).startswith("NWL"):
            pixel = {
                f"{str(self.__prod.value)}_JASMES": self.__handle_digital_number()[row, col],
                f"{str(self.__prod.value).replace('NWLR', 'Rrs')}_JASMES": self.__handle_digital_number(rrs=True)[row, col]
            }
        else:
            pixel = {
                f"{str(self.__prod.value)}_JASMES": self.__handle_digital_number()[row, col],
            }
        return pixel