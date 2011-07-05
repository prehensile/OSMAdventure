import GeoUtilities
import OsmApi
import OSMUtilities
import math
import AdventureUtilities
import AdventureClient

# baker street
lat = 51.522
long = -0.157

# rushmore road
#lat = 51.55464
#long = -0.05068

osm_connector = OsmApi.OsmApi()

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

sorted_items = OSMUtilities.sorted_items_by_distance( map, lat, long )

# get nearest Way & Node
current_way = None
current_node = None
for item in sorted_items:
	id = OSMUtilities.id_for_item( item )
	if( id ):
		ways = osm_connector.NodeWays( id )
		for way in ways:
			name = OSMUtilities.name_for_data( way )
			if( name ):
				current_way = way
				current_node = OSMUtilities.data_for_item( item )
				break
		if( current_way is not None ):
			break
			
# get node list for current Way
id_current_node = OSMUtilities.id_for_data( current_node )
way_nodes = osm_connector.WayGet( current_way[ OSMUtilities.key_id ] )
nd_current_way = way_nodes[ OSMUtilities.key_nd ]

# game loop
node_in = current_node
way_in = current_way
nd_in = nd_current_way
while( 1 ):
	node_out, way_out, nd_out = AdventureClient.go_to_node( osm_connector, node_in, way_in, nd_in )
	node_in = node_out
	way_in = way_out
	nd_in = nd_out