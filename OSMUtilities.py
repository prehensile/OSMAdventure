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
key_amenity = u'amenity'

geod = pyproj.Geod(ellps='clrk66')

def latlong_for_data( data ):
	lat = data[ key_lat ]
	lon = data[ key_lon ]
	return lat, lon

def node_bearing( node1, node2 ):
	lat1, lon1 = latlong_for_data( node1 )
	lat2, lon2 = latlong_for_data( node2 )
	# a = GeoUtilities.haversine_bearing( lon1, lat1, lon2, lat2 )
	# a = GeoUtilities.williams_bearing( lat1, lon1, lat2, lon2 )
	a = geod.inv( lon1, lat1, lon2, lat2 )[0]
	a = (a+math.pi) % (math.pi*2) # normalise heading
	# print "-->%2.8f" % a
	# print "--->%2.8f" % math.degrees( a )
	return( a )

def node_distance( node1, node2 ):
	lat1, lon1 = latlong_for_data( node1 )
	lat2, lon2 = latlong_for_data( node2 )
	d = geod.inv( lon1, lat1, lon2, lat2 )[2]
	return( d )

def type_for_item( data ):
	type_out = None
	if( key_type in data ):
		type_out = data[ key_type ]
	return type_out

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

def tag_for_item( item ):
	data = data_for_item( item )
	return tag_for_data( data )

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
		item_lat, item_lon = latlong_for_data( data )
		# d = GeoUtilities.distance( lat, lon, item_lat, item_lon )
		# d = GeoUtilities.haversine_distance( lon, lat, item_lon, item_lat )
		d = geod.inv( lon, lat, item_lon, item_lat )[2]
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


def get_nearest_node_to_latlong( osm_connector, lat, long ):

	# get nearby things
	map = []
	dist = .02
	way = None
	i = 0
	while( len( map ) < 10 ):
		bbox = GeoUtilities.boundingBox( lat, long, dist )
		map = osm_connector.Map( bbox[ "lonMin" ], bbox[ "latMin" ], bbox[ "lonMax" ], bbox[ "latMax" ] )
		dist = dist * 1.5
		i = i + 1 
	
	sorted_items = sorted_items_by_distance( map, lat, long )
	
	# get nearest Way & Node
	current_way = None
	current_node = None
	for item in sorted_items:
		id = id_for_item( item )
		if( id ):
			ways = osm_connector.NodeWays( id )
			for way in ways:
				name = name_for_data( way )
				if( name ):
					current_way = way
					current_node = data_for_item( item )
					break
			if( current_way is not None ):
				break
	
	return current_node, current_way


class OSMNode:
	
	def __init__( self, data_in ):
		self.data = data_in
		self.tag = tag_for_data( data_in )
		self.name = None
	
	def get_id( self ):
		return( self.data[ key_id ] )
	
	def get_name( self ):
		if( self.name is None and self.tag ):
			self.name = name_for_tag( self.tag )
		return( self.name )