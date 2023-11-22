"""
This module provide interface for extracting the pixel value out of an SGLI product using lat and long
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""

from pathlib import Path
from jasmes import JASMESProd
from .extractor_interface import Extractor
from .utils import find_entry
import numpy as np
from netCDF4 import Dataset
import warnings



class JASMESExtractor(Extractor):
    def __init__(self, path: Path, prod:JASMESProd):
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
        errors = data[:].mask
        with warnings.catch_warnings():
            warnings.filterwarnings(
                'ignore', r'invalid value encountered in (greater|less)')
            errors[data[:].data > data.Maximum_valid_DN] = True
            errors[data[:].data < data.Minimum_valid_DN] = True

        # Convert DN to physical value
        if rrs:
            scale = data.Rrs_scale_factor
            offset = data.Rrs_add_offset
            digital_data = (data[:].data - data.add_offset)/data.scale_factor
            physical_data = digital_data * scale + offset
        else:
            physical_data = data[:].data
        physical_data[errors] = np.nan
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
        print(row, col)
        if str(self.__prod.value).startswith("NWL"):
            pixel = {
                f"{str(self.__prod.value)}": self.__handle_digital_number()[row, col],
                f"{str(self.__prod.value).replace('NWLR', 'Rrs')}": self.__handle_digital_number(rrs=True)[row, col]
            }
        else:
            pixel = {
                f"{str(self.__prod.value)}": self.__handle_digital_number()[row, col],
            }
        return pixel