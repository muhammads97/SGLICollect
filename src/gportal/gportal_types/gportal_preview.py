"""
Author: Muhammad Salah
Email: msalah.29.10@gmail.com
"""
from enum import Enum
from urllib.parse import urlparse, ParseResult


class GPortalPreviewType(Enum):
    QUICKLOOK = "QUICKLOOK"
    THUMBNAIL = "THUMBNAIL"


class GPortalPreview:
    type: GPortalPreviewType
    url: ParseResult

    def __init__(self, response) -> None:
        """
        parser for GPortal preview instance response (browse)
        
        :response dict the json dictionary of the response (browse)
        """
        self.type = GPortalPreviewType(response["type"])
        self.url = urlparse(response["fileName"])

    def to_json(self) -> dict:
        return {
            "type": self.type.value,
            "url": self.url.geturl()
        }
