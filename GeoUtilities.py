import math

###
## from http://www.geesblog.com/2009/01/calculating-distance-between-latitude-longitude-pairs-in-python/
#

#
# The following formulas are adapted from the Aviation Formulary
# http://williams.best.vwh.net/avform.htm
#
nauticalMilePerLat = 60.00721
nauticalMilePerLongitude = 60.10793
rad = math.pi / 180.0
milesPerNauticalMile = 1.15078
kmPerNauticalMile = 1.85200
def distance(lat1, lon1, lat2, lon2):
	"""
	Caclulate distance between two lat lons in NM
	"""
	yDistance = (lat2 - lat1) * nauticalMilePerLat
	xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * (nauticalMilePerLongitude / 2)
	distance = math.sqrt( yDistance**2 + xDistance**2 )
	# return distance * milesPerNauticalMile
	return distance * kmPerNauticalMile

###
## from http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points/4913653#4913653
#
	"""
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
	"""

def haversine_bearing(lon1, lat1, lon2, lat2):
	# print "haversine_bearing( %2.8f, %2.8f, %2.8f, %2.8f )" % ( lon1, lat1, lon2, lat2 )
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
	# print "-> %2.8f, %2.8f, %2.8f, %2.8f" % ( lon1, lat1, lon2, lat2 )
	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
	# print "-->%2.8f" % a
	return a 

def haversine_distance(lon1, lat1, lon2, lat2):
    a = haversine_bearing(lon1, lat1, lon2, lat2)
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a)) 
    km = 6367 * c
    return km 

def williams_bearing( lat1, lon1, lat2, lon2 ):
	lat1 = math.radians( lat1 )
	lat2 = math.radians( lat2 )
	dLon = math.radians(lon2-lon1)
	y = math.sin(dLon) * math.cos(lat2)
	x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon)
	return math.atan2( y, x );

###
## from http://stackoverflow.com/questions/238260/how-to-calculate-the-bounding-box-for-a-given-lat-lng-location
#

# degrees to radians
def deg2rad(degrees):
    return math.pi*degrees/180.0
# radians to degrees
def rad2deg(radians):
    return 180.0*radians/math.pi

# Semi-axes of WGS-84 geoidal reference
WGS84_a = 6378137.0  # Major semiaxis [m]
WGS84_b = 6356752.3  # Minor semiaxis [m]

# Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
def WGS84EarthRadius(lat):
    # http://en.wikipedia.org/wiki/Earth_radius
    An = WGS84_a*WGS84_a * math.cos(lat)
    Bn = WGS84_b*WGS84_b * math.sin(lat)
    Ad = WGS84_a * math.cos(lat)
    Bd = WGS84_b * math.sin(lat)
    return math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )

# Bounding box surrounding the point at given coordinates,
# assuming local approximation of Earth surface as a sphere
# of radius given by WGS84
def boundingBox(latitudeInDegrees, longitudeInDegrees, halfSideInKm):
    lat = deg2rad(latitudeInDegrees)
    lon = deg2rad(longitudeInDegrees)
    halfSide = 1000*halfSideInKm

    # Radius of Earth at given latitude
    radius = WGS84EarthRadius(lat)
    # Radius of the parallel at given latitude
    pradius = radius*math.cos(lat)

    latMin = lat - halfSide/radius
    latMax = lat + halfSide/radius
    lonMin = lon - halfSide/pradius
    lonMax = lon + halfSide/pradius

    return ({ "latMin": rad2deg(latMin), "lonMin": rad2deg(lonMin), "latMax": rad2deg(latMax), "lonMax": rad2deg(lonMax) })