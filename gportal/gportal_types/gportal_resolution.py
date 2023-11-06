from enum import Enum
class GPortalResolution(Enum):
    H = "250m"
    L = "1km"

    def from_str(s:str):
        if s.startswith("250"):
            return GPortalResolution.H
        elif s.startswith("1"):
            return GPortalResolution.L
    
    def from_int(i:int):
        if i == 250:
            return GPortalResolution.H
        elif i == 1 or i == 1000:
            return GPortalResolution.L
