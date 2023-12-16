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
