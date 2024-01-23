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


class GPortalGeo:
    type: str
    coordinates: list[list[float]]

    def __init__(self, response:dict) -> None:
        """
        parser for GPortal Geo response
        
        :response dict the json dictionary of the response
        """
        self.type = str(response["type"])
        self.coordinates = [[float(entry) for entry in part]
                            for part in response["coordinates"][0]]

    def to_json(self) -> dict:
        return {
            "type": self.type,
            "coordinates": self.coordinates
        }
