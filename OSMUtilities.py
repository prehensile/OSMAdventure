import GeoUtilities
import math
import pyproj

key_data = "data"
key_name = "name"
key_tag = "tag"
key_lat = "lat"
key_lon = "lon"
key_type = "type"
type_way = u'way'
type_node = u'node'
key_id = "id"
key_nd = "nd"
key_highway = "highway"

def node_bearing( node1, node2 ):
	lat1 = node1[ key_lat ]
	lon1 = node1[ key_lon ]
	lat2 = node2[ key_lat ]
	lon2 = node2[ key_lon ]
	# a = GeoUtilities.haversine_bearing( lon1, lat1, lon2, lat2 )
	# a = GeoUtilities.williams_bearing( lat1, lon1, lat2, lon2 )
	g1 = pyproj.Geod(ellps='clrk66')
	az12,az21,dist = g1.inv( lon1, lat1, lon2, lat2, True )
	a = az12
	a = (a+math.pi) % (math.pi*2) # normalise heading
	# print "-->%2.8f" % a
	# print "--->%2.8f" % math.degrees( a )
	return( a )

def data_for_item( item ):
	data = None
	if( key_data in item ):
		data = item[ key_data ]
	return( data )

def id_for_data( data ):
	id = None
	if( data and key_id in data ):
		id = data[ key_id ]
	return( id )

def id_for_item( item ):
	data = data_for_item( item )
	return id_for_data( data )

def tag_for_data( data ):
	tag = None
	if( data and key_tag in data ):
		tag = data[ key_tag ]
	return( tag )

def name_for_tag( tag ):
	name = None
	if( tag and key_name in tag ):
		name = tag[ key_name ]
	return( name )

def name_for_data( data ):
	tag = tag_for_data( data )
	return name_for_tag( tag ) 

def item_distance( item, lat, lon ):
	d = 0
	data = item[ key_data ]
	if( key_lat in data ):
		item_lat = data[ key_lat ]
		item_lon = data[ key_lon ]
		# d = GeoUtilities.distance( lat, lon, item_lat, item_lon )
		d = GeoUtilities.haversine_distance( lon, lat, item_lon, item_lat )
	return( d )

def sorted_items_by_distance( items_in, lat, long ):
	sorted_items = []
	# shitty sorting
	for item in items_in:
		data = item[ key_data ]
		if( key_lat in data ):
			d1 = item_distance( item, lat, long )
			l = len( sorted_items )
			i = 0
			hasInserted = False
			while( i < l ):
				sorted_item = sorted_items[ i ]
				d2 = item_distance( sorted_item, lat, long )
				if( d1 < d2 ):
					sorted_items.insert( i, item )
					hasInserted = True
					break
				i = i + 1
			if( hasInserted is False ):
				sorted_items.append( item )
	return( sorted_items )