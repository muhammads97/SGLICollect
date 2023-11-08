"""
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""
from enum import Enum
class GPortalResolution(Enum):
    H = "250m"
    L = "1km"

    def from_str(s:str):
        """
        convert string to resolution.

        return None or GPortalResolution

        :s str string representation of the resolution 250m or 1km
        """
        if s.startswith("250"):
            return GPortalResolution.H
        elif s.startswith("1"):
            return GPortalResolution.L
    
    def from_int(i:int):
        """
        convert integer to resolution.

        return None or GPortalResolution

        :i int integer representation of the resolution 250 or 1000
        """
        if i == 250:
            return GPortalResolution.H
        elif i == 1 or i == 1000:
            return GPortalResolution.L
