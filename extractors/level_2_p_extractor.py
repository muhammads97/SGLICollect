from pathlib import Path
from .extractor_interface import Extractor
from .utils import find_entry
import numpy as np



class GPortalL2PExtractor(Extractor):
    __FLAGS: list[str] = ['DATAMISS', 'LAND', 'ATMFAIL', 'CLDICE', 'CLDAFFCTD', 
                        'STRAYLIGHT', 'HIGLINT', 'MODGLINT', 'HISOLZ', 'HISENZ', 
                        'TURBIDW', 'SHALLOW', 'ITERFAILCDOM', 'CHLWARN', 'LOWNLW'
                        ]
        
    def __digital_number_to_prod(self, prod_name:str) -> np.ndarray[float, float]:
        # Get product data
        real_prod_name = prod_name.capitalize()
        data = self.__h5['Image_data/' + real_prod_name]

        # Validate
        prod = data[:].astype(np.float32)
        if 'Error_DN' in data.attrs:
            prod[prod == data.attrs['Error_DN'][0]] = np.NaN
        with np.warnings.catch_warnings():
            np.warnings.filterwarnings(
                'ignore', r'invalid value encountered in (greater|less)')
            if 'Maximum_valid_DN' in data.attrs:
                prod[prod > data.attrs['Maximum_valid_DN'][0]] = np.NaN
            if 'Minimum_valid_DN' in data.attrs:
                prod[prod < data.attrs['Minimum_valid_DN'][0]] = np.NaN

        # Convert DN to physical value
        slope = data.attrs['Slope'][0]
        offset = data.attrs['Offset'][0]
        prod = prod * slope + offset
        return prod
        
    def __calculate_flags(self, flags_value: int) -> dict:
        flags = {}
        order = 0
        while order < 15:
            flags[self.__FLAGS[order]] = flags_value % 2
            flags_value //= 2
            order += 1
        return flags

    def get_pixel(self, lat:float, lon:float) -> dict:
        lat_mat, lon_mat = self.get_lat_lon()
        row, col, distance = find_entry(lat_mat, lon_mat, lat, lon)
        print("=> matching point with distance^2 = %f" % (distance))
        flags = self.__calculate_flags(self.__h5["Image_data/QA_flag"][row, col])
        pixel = {
            "Chla": self.__digital_number_to_prod("Chla")[row, col],
            "aCDOM_412": self.__digital_number_to_prod("CDOM")[row, col],
            "TSM": self.__digital_number_to_prod("TSM")[row, col],
        }
        pixel.update(flags)
        return pixel


