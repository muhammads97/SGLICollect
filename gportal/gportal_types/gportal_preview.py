from enum import Enum
from urllib.parse import urlparse, ParseResult


class GPortalPreviewType(Enum):
    QUICKLOOK = "QUICKLOOK"
    THUMBNAIL = "THUMBNAIL"


class GPortalPreview:
    type: GPortalPreviewType
    url: ParseResult

    def __init__(self, response) -> None:
        self.type = GPortalPreviewType(response["type"])
        self.url = urlparse(response["fileName"])

    def to_json(self) -> dict:
        return {
            "type": self.type.value,
            "url": self.url.geturl()
        }
