RAD_TO_DEGREE = 57.29577951307855

LON_START = 0.203125
LON_LEN = 0.25
LON_ST = LON_LEN / 1048576

LAT_START = 0.84375
LAT_LEN = 0.125
LAT_ST = LAT_LEN / 1048576

def rad_to_deg(a_radians):
    return a_radians * RAD_TO_DEGREE

def lon_to_lon(a_lon):
    return round(rad_to_deg(LON_ST * a_lon + LON_START) * 1000000 / 1000000, 6)

def lat_to_lat(a_lat):
    return round(rad_to_deg(LAT_ST * a_lat + LAT_START) * 1000000 / 1000000, 6)

def get_position(la, lo):
    return (lat_to_lat(la), lon_to_lon(lo))
