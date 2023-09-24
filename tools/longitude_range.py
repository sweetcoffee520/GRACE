import numpy as np

def longitude_range(lon,lon_range):

    if lon_range[0]>lon_range[1]:
        lonm = (lon<=lon_range[0]|(lon>=lon_range[1]))
    else:
        lonm = (lon>=lon_range[0])&(lon<=lon_range[1])

    return lonm