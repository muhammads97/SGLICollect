"""
This module provide interface for extracting the pixel value out of an SGLI product using lat and long
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""

from .extractor_interface import Extractor
from .utils import find_entry
import numpy as np



class GPortalL1BExtractor(Extractor):
        
    def __handle_digital_number(self, prod_name:str) -> np.ndarray[float, float]:
        """
        Convert digital number to the desired product

        :prod_name str the desired product (Lt01 to Lt11 for radiance) or (Rt01 to Rt11 for reflectance)
        """
        # Get data
        if prod_name.startswith("L"):
            radiance = True

        if radiance: real_prod_name = prod_name.replace('Lt_VN', 'Lt')
        else: real_prod_name = prod_name.replace('Lt_VN', 'Rt')

        data = self.__h5['Image_data/' + real_prod_name]
        rad = data[:].astype(np.float32)

        # Validate
        rad[rad == data.attrs['Error_DN'][0]] = np.NaN
        with np.warnings.catch_warnings():
            np.warnings.filterwarnings(
                'ignore', r'invalid value encountered in (greater|less)')
            rad[rad > data.attrs['Maximum_valid_DN'][0]] = np.NaN
            rad[rad < data.attrs['Minimum_valid_DN'][0]] = np.NaN

        # Convert DN to physical value
        if radiance:
            slope = data.attrs['Slope'][0]
            offset = data.attrs['Offset'][0]
        else:
            slope = data.attrs['Slope_reflectance'][0]
            offset = data.attrs['Offset_reflectance'][0]
        mask = data.attrs['Mask']

        rad = (rad&mask) * slope + offset
        return rad

    def get_pixel(self, lat:float, lon:float) -> dict:
        lat_mat, lon_mat = self.get_lat_lon()
        row, col, distance = find_entry(lat_mat, lon_mat, lat, lon)
        print("=> matching point with distance^2 = %f" % (distance))
        pixel = {
            "Lt01": self.__handle_digital_number("Lt01")[row, col],
            "Lt02": self.__handle_digital_number("Lt02")[row, col],
            "Lt03": self.__handle_digital_number("Lt03")[row, col],
            "Lt04": self.__handle_digital_number("Lt04")[row, col],
            "Lt05": self.__handle_digital_number("Lt05")[row, col],
            "Lt06": self.__handle_digital_number("Lt06")[row, col],
            "Lt07": self.__handle_digital_number("Lt07")[row, col],
            "Lt08": self.__handle_digital_number("Lt08")[row, col],
            "Lt09": self.__handle_digital_number("Lt09")[row, col],
            "Lt10": self.__handle_digital_number("Lt10")[row, col],
            "Lt11": self.__handle_digital_number("Lt11")[row, col],
            "Rt01": self.__handle_digital_number("Rt01")[row, col],
            "Rt02": self.__handle_digital_number("Rt02")[row, col],
            "Rt03": self.__handle_digital_number("Rt03")[row, col],
            "Rt04": self.__handle_digital_number("Rt04")[row, col],
            "Rt05": self.__handle_digital_number("Rt05")[row, col],
            "Rt06": self.__handle_digital_number("Rt06")[row, col],
            "Rt07": self.__handle_digital_number("Rt07")[row, col],
            "Rt08": self.__handle_digital_number("Rt08")[row, col],
            "Rt09": self.__handle_digital_number("Rt09")[row, col],
            "Rt10": self.__handle_digital_number("Rt10")[row, col],
            "Rt11": self.__handle_digital_number("Rt11")[row, col],
            "land": self.__h5["Image_data"]["Land_water_flag"][:][row, col]
        }            
        return pixel


