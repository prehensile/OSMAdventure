import GeoUtilities
import OsmApi
import OSMUtilities
import math
import AdventureUtilities
import AdventureClient

def go_to_node( osm_connector, node_in, way_in, nd_in ):
	
	# print "go_to_node:\n\t%s\n\t%s\n\t%s\n\t%s" % ( osm_connector, node_in, way_in, nd_in )
	
	node_id = OSMUtilities.id_for_data( node_in )
	
	# get ptr to current nd
	ptr_nd = -1
	i = 0
	for nd in nd_in:
		if( nd == node_id ):
			ptr_nd = i
			break
		i = i + 1

	
	# start description output
	#print "DEBUG"
	#print "current node: %s" % node_in
	out = "%s (waypoint #%d).\n" % ( AdventureUtilities.description_for_way( way_in ), (ptr_nd + 1) )
	out += "You are standing "
	
	# describe ways
	ways = osm_connector.NodeWays( node_id )
	desc_ways = ""
	l = len( ways )
	if( l > 1 ):
		descriptions = []
		for way in ways:
			description = AdventureUtilities.description_for_way( way )
			descriptions.append( description )
		joined = " and ".join( descriptions )
		desc_ways = "at the intersection of %s" % joined
	else:
		desc_ways = "on %s" % AdventureUtilities.description_for_way( ways[0] )
	out += "%s.\n" % desc_ways
	
	# describe things
	# rel = osm_connector.NodeRelations( id )
	# print "relationships: %s" % rel
	
	# build connections
	next_node = None
	prev_node = None
	bearing_next = -1;
	bearing_prev = -1;
	
	if( ptr_nd < len( nd_in ) -1 ):
		id_next = nd_in[ ptr_nd + 1 ]
		next_node = osm_connector.NodeGet( id_next )
		# print "next node: %s" % next_node
		bearing_next = OSMUtilities.node_bearing( node_in, next_node )
	
	if( ptr_nd > 0 ):
		id_prev = nd_in[ ptr_nd - 1 ]
		prev_node = osm_connector.NodeGet( id_prev )
		#print "previous node: %s" % prev_node
		bearing_prev = OSMUtilities.node_bearing( node_in, prev_node )
	
	desc_ways_out = "%s continues to the " % AdventureUtilities.description_for_way( way_in )
	ways_out = {}
	
	if( next_node ):
		cardinal_next = AdventureUtilities.cardinal_for_bearing( bearing_next )
		ways_out[ cardinal_next ] = ( next_node, way_in, nd_in )
		desc_ways_out += AdventureUtilities.description_for_cardinal( cardinal_next )
		if( prev_node ):
			desc_ways_out += " and "
	
	if( prev_node ):
		cardinal_prev = AdventureUtilities.cardinal_for_bearing( bearing_prev )
		ways_out[ cardinal_prev ] = ( prev_node, way_in, nd_in )
		desc_ways_out += AdventureUtilities.description_for_cardinal( cardinal_prev )
		
	out += "%s." % desc_ways_out
	
	print out
	input = raw_input(">")
	
	if( input in ways_out ):
		way_out = ways_out[ input ]
		return( way_out )
	
	return None