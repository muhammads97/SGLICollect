"""
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""
from urllib.parse import urlparse, ParseResult


class GPortalProduct:
    downloadUrl: ParseResult
    size: int
    formatType: str
    version: int

    def __init__(self, response: dict) -> None:
        """
        parser for GPortal product response (product)
        
        :response dict the json dictionary of the response (product)
        """
        self.downloadUrl = urlparse(response["fileName"])
        self.size = int(response["size"])
        self.formatType = response["DataFormatType"]
        self.version = int(response["version"])

    def to_json(self) -> dict:
        return {
            "downloadUrl": self.downloadUrl.geturl(),
            "size": self.size,
            "formatType": self.formatType,
            "version": self.version
        }
