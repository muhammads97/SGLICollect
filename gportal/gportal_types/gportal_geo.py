"""
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""
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
