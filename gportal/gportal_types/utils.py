def int_or_none(s:str):
    try:
        return int(s)
    except:
        return None

def float_or_none(s:str):
    try:
        return float(s)
    except:
        return None