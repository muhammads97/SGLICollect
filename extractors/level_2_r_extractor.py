from pathlib import Path
from .extractor_interface import Extractor
from .utils import find_entry
import numpy as np



class GPortalL2RExtractor(Extractor):
    __FLAGS: list[str] = ['DATAMISS', 'LAND', 'ATMFAIL', 'CLDICE', 'CLDAFFCTD', 
                        'STRAYLIGHT', 'HIGLINT', 'MODGLINT', 'HISOLZ', 'HITAUA', 
                        'EPSOUT', 'OVERITER', 'NEGNLW', 'HIGHWS', 'TURBIDW'
                        ]
        
    def __digital_number_to_rrs(self, prod_name:str) -> np.ndarray[float, float]:
        # Get Rrs data
        real_prod_name = prod_name.replace('Rrs', 'NWLR')
        data = self.__h5['Image_data/' + real_prod_name]

        # Validate
        rrs = data[:].astype(np.float32)
        if 'Error_DN' in data.attrs:
            rrs[rrs == data.attrs['Error_DN'][0]] = np.NaN
        with np.warnings.catch_warnings():
            np.warnings.filterwarnings(
                'ignore', r'invalid value encountered in (greater|less)')
            if 'Maximum_valid_DN' in data.attrs:
                rrs[rrs > data.attrs['Maximum_valid_DN'][0]] = np.NaN
            if 'Minimum_valid_DN' in data.attrs:
                rrs[rrs < data.attrs['Minimum_valid_DN'][0]] = np.NaN

        # Convert DN to physical value
        slope = data.attrs['Rrs_slope'][0]
        offset = data.attrs['Rrs_offset'][0]
        rrs = rrs * slope + offset
        return rrs
        
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

            "Rrs_380": self.__digital_number_to_rrs("Rrs_380")[row, col],
            "Rrs_412": self.__digital_number_to_rrs("Rrs_412")[row, col],
            "Rrs_443": self.__digital_number_to_rrs("Rrs_443")[row, col],
            "Rrs_490": self.__digital_number_to_rrs("Rrs_490")[row, col],
            "Rrs_530": self.__digital_number_to_rrs("Rrs_530")[row, col],
            "Rrs_565": self.__digital_number_to_rrs("Rrs_565")[row, col],
            "Rrs_670": self.__digital_number_to_rrs("Rrs_670")[row, col],
        }
        pixel.update(flags)
        return pixel


