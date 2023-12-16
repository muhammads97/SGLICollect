#
# Copyright (c) 2023 Muhammad Salah msalah.29.10@gmail.com
# Licensed under AGPL-3.0-or-later.
# Refer to COPYING.txt for the AGPL license.
# All rights reserved.
# This project is developed as part of my research in the Remote Sensing Laboratory
# in Kyoto University of Advanced Science towards my Master's Degree course.
# The research was mainly supervised by Professor Salem Ibrahim Salem.
#

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
