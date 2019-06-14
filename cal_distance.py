import math


def calculate_distance(lat, lng, lat1, lng1):

    '''
    calculate the distance between two points
    :param lat: the latitude of first point
    :param lng: the longitude of first point
    :param lat1: the latitude of second point
    :param lng1: the longitude of second point
    :return: distance in kilometer
    '''

    def rad(d):
        return float(d) * (math.pi / 180.0)

    EARTH_RADIUS = 6378.137
    radLat = rad(lat)
    radLat1 = rad(lat1)
    radLng = rad(lng)
    radLng1 = rad(lng1)
    a = radLat - radLat1
    b = radLng - radLng1
    s = 2 * math.asin(
        math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(radLat) * math.cos(radLat1) * math.pow(math.sin(b / 2), 2)))
    distance = s * EARTH_RADIUS
    return distance
