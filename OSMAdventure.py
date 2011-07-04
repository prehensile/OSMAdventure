import OsmApi
import GeoUtilities

# baker street
lat = 51.522
long = -0.157

key_data = "data"
key_name = "name"
key_tag = "tag"
key_lat = "lat"
key_lon = "lon"
key_type = "type"
type_way = u'way'
type_node = u'node'
key_id = "id"

def item_distance( item, lat, lon ):
	d = 0
	data = item[ key_data ]
	if( key_lat in data ):
		item_lat = data[ key_lat ]
		item_lon = data[ key_lon ]
		d = GeoUtilities.distance( lat, lon, item_lat, item_lon )
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

def getNearestWay( lat, long ):
	# get nearby things
	map = []
	dist = .02
	way = None
	i = 0
	while( len( map ) < 10 ):
		bbox = GeoUtilities.boundingBox( lat, long, dist )
		map = OSMConnector.Map( bbox[ "lonMin" ], bbox[ "latMin" ], bbox[ "lonMax" ], bbox[ "latMax" ] )
		dist = dist * 1.5
		i = i + 1 
	
	sorted_items = sorted_items_by_distance( map, lat, long )
	
	# get nearest Way
	current_way = None
	for item in sorted_items:
		data = item[ key_data ]
		id = data[ key_id ]
		ways = OSMConnector.NodeWays( id )
		for way in ways:
			tag = way[ key_tag ]
			if( key_name in tag ):
				current_way = way
				break
		if( current_way is not None ):
			break
	
	return( current_way )

	
OSMConnector = OsmApi.OsmApi()


if( current_way ):
	tag = way[ key_tag ]
	name = tag[ key_name ]
	print name
