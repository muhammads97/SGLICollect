#
# Copyright (c) 2023 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#

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
