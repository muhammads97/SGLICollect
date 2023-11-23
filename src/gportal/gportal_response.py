"""
Parser for GPortal API search results
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""
import numpy as np
from src.gportal.gportal_types import GPortalProperties, GPortalGeo
from src.utils import inside_polygon, min_distance
from pathlib import Path
import pandas as pd

OUTPUT_COLUMNS = [
    "identifier",
    "file_status",
    "resolution",
    "download_url",
    "preview_url",
    "cloud_coverage"
]


class GPortalResponse:
    type: str
    geometry: GPortalGeo
    properties: GPortalProperties

    def __init__(self, response:dict) -> None:
        """
        parse the response of one result returned from GPortal
        
        :response dictionary of the json response
        """
        self.type = str(response["type"])
        self.geometry = GPortalGeo(response["geometry"])
        self.properties = GPortalProperties(response["properties"])

    def to_json(self) -> dict:
        """convert it to json"""
        return {
            "type": self.type,
            "geometry": self.geometry.to_json(),
            "properties": self.properties.to_json()
        }
    
    def to_dataframe(self, df:pd.DataFrame=None, index:int=None):
        """
        appends the response to a dataframe in index
        """
        if df is None:
            df = pd.DataFrame(columns=OUTPUT_COLUMNS)
        if index is None:
            index = 0
            for c in OUTPUT_COLUMNS:
                if c not in df.columns:
                    df[c] = []
        if(index == df.size):
            j = pd.DataFrame([{
                "identifier"    : self.properties.identifier,
                "file_status"   : self.properties.status,
                "resolution"    : self.properties.resolution,
                "download_url"  : self.properties.product.downloadUrl.geturl(),
                "preview_url"   : self.properties.previews[0].url.geturl(),
                "cloud_coverage": self.properties.meta.cloudCoverPercentage
            }], columns=OUTPUT_COLUMNS)
            df = pd.concat([df, j], axis=0, ignore_index=True)
        else:
            index = df.index[index]
            df.loc[index, "identifier"] = self.properties.identifier
            df.loc[index, "file_status"]=self.properties.status
            df.loc[index, "resolution"]=self.properties.resolution
            df.loc[index, "download_url"]=self.properties.product.downloadUrl.geturl()
            df.loc[index, "preview_url"]=self.properties.previews[0].url.geturl()
            df.loc[index, "cloud_coverage"]=self.properties.meta.cloudCoverPercentage
        return df
    

    def save(self, path: Path):
        """
        saves to csv file
        """
        try:
            df = pd.read_csv(path)
        except:
            df = None
        df = self.to_dataframe(df)
        df.to_csv(path)
        return df
    def print(self):
        """
        prints the product to screen
        """
        print(
            "ID: %s"%self.properties.identifier,
            "status: %s"%self.properties.status,
            "resolution: %s"%self.properties.resolution,
            "download: %s"%self.properties.product.downloadUrl.geturl(),
            "preview: %s"%self.properties.previews[0].url.geturl(),
            "cloud: %s"%self.properties.meta.cloudCoverPercentage,
            sep="\n"
        )



class GPortalSearchResult:
    results: list[GPortalResponse]
    def __init__(self, response:dict) -> None:
        """
        parses the returned results from GPortal
        """
        self.results = [GPortalResponse(f) for f in response["features"]]

    def filter_results(self, lat:float, lon:float) -> GPortalResponse:
        """
        Filters the results to make sure the given latitude and longitude are within the product coordinates.
        Then selects the product in which the given latitude and longitude are closer to the center.

        | lat         : float latitude
        | lon         : float longitude

        return None if no results
        """
        if len(self.results) == 0: return None

        filtered: list[GPortalResponse] = [] # contains all the products that INCLUDE the given lat and lon
        for f in self.results:
            poly = f.geometry.coordinates
            poly = np.array(poly)
            poly = poly.T
            if inside_polygon(poly[0], poly[1], lon, lat):
                filtered.append(f)
        if len(filtered) > 1:
            boarder_dis = []
            point = [lat, lon]
            for i in range(len(filtered)):
                polygon = filtered[i].geometry.coordinates
                boarder_dis.append(min_distance(point, polygon))
            j = boarder_dis.index(max(boarder_dis)) # index of the product with lat and lon closest to center
        else:
            j = 0
        if len(filtered) == 0: return None
        return filtered[j]
    
    