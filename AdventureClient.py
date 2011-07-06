import GeoUtilities
import OsmApi
import OSMUtilities
import math
import AdventureUtilities
import AdventureClient
from sets import Set


def get_neighbours( osm_connector, node, way ):
	
	result = osm_connector.WayGet( way[ OSMUtilities.key_id ] )
	nodelist = result[ OSMUtilities.key_nd ]
	
	# get ptr to current nd
	node_id = OSMUtilities.id_for_data( node )
	ptr_nd = -1
	i = 0
	for nd in nodelist:
		if( nd == node_id ):
			ptr_nd = i
			break
		i = i + 1
	
	prev_node = None
	next_node = None
	
	if( ptr_nd < len( nodelist ) -1 ):
		id_next = nodelist[ ptr_nd + 1 ]
		next_node = osm_connector.NodeGet( id_next )
	
	if( ptr_nd > 0 ):
		id_prev = nodelist[ ptr_nd - 1 ]
		prev_node = osm_connector.NodeGet( id_prev )
		
	return prev_node, next_node
	

def go_to_node( osm_connector, node_in, way_in  ):
	
	node_id = OSMUtilities.id_for_data( node_in )
	
	# step through ways
	ways = osm_connector.NodeWays( node_id )
	desc_ways = ""
	desc_ways_out = ""
	ways_out = {}
	way_names = Set([])
	id_way_in =  OSMUtilities.id_for_data( way_in )
		
	for nodeway in ways:
		way_id = OSMUtilities.id_for_data( nodeway )
		way_name = AdventureUtilities.description_for_way( nodeway )
		way_names.add( way_name )
		
		prev_node, next_node = get_neighbours( osm_connector, node_in, nodeway )
		bearing_next = -1;
		bearing_prev = -1;
		
		if( way_id == id_way_in ):
			desc_ways_out += "%s runs to the " % AdventureUtilities.description_for_way( nodeway, False, True ).capitalize()
		else: 
			desc_ways_out += "%s goes off to the " % way_name.capitalize()
			
		if( next_node ):
			bearing_next = OSMUtilities.node_bearing( node_in, next_node )
			cardinal_next = AdventureUtilities.cardinal_for_bearing( bearing_next )
			ways_out[ cardinal_next ] = ( next_node, nodeway )
			desc_ways_out += AdventureUtilities.description_for_cardinal( cardinal_next )
			if( prev_node ):
				desc_ways_out += " and "
		
		if( prev_node ):
			bearing_prev = OSMUtilities.node_bearing( node_in, prev_node )
			cardinal_prev = AdventureUtilities.cardinal_for_bearing( bearing_prev )
			ways_out[ cardinal_prev ] = ( prev_node, nodeway )
			desc_ways_out += AdventureUtilities.description_for_cardinal( cardinal_prev )
		
		desc_ways_out +=".\n"
	
	if( len( way_names ) > 1 ):
		joined = " and ".join( way_names )
		desc_ways = "at the intersection of %s" % joined
	else:
		desc_ways = "on %s" % way_names.copy().pop()
	
	# start description output
	#print "DEBUG"
	#print "current node: %s" % node_in
	out = "%s.\n" % ( AdventureUtilities.description_for_way( way_in, True ) )
	out += "You are standing %s.\n" % desc_ways
	out += desc_ways_out
	
	# describe things
	# rel = osm_connector.NodeRelations( id )
	# print "relationships: %s" % rel
	
	return out, ways_out