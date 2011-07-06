import GeoUtilities
import OsmApi
import OSMUtilities
import math
import AdventureUtilities
import AdventureClient
from sets import Set
from DebugUtilities import DebugUtilities

def go_to_node( osm_connector, node_in, way_in  ):
	
	node_id = OSMUtilities.id_for_data( node_in )
	
	# step through ways
	ways = osm_connector.NodeWays( node_id )
	desc_ways = ""
	desc_ways_out = ""
	ways_out = {}
	way_names = Set([])
	id_way_in =  OSMUtilities.id_for_data( way_in )
	scratch_string = ""
		
	for nodeway in ways:
		way_id = OSMUtilities.id_for_data( nodeway )
		way_name = AdventureUtilities.description_for_way( nodeway )
		way_names.add( way_name )
		
		prev_node, next_node = AdventureUtilities.get_neighbours( osm_connector, node_in, nodeway )
		bearing_next = -1;
		bearing_prev = -1;
		
		str_go = ""
		str_name = way_name
		if( way_id == id_way_in ):
			str_go = "runs"
			str_name = AdventureUtilities.description_for_way( nodeway, False, True )
			str_name = AdventureUtilities.ucfirst( str_name )
			if( str_name[-1:] == "s" ):
				str_go = "run"
		else: 
			str_go = "goes off"
			str_name = AdventureUtilities.ucfirst( way_name )
			if( str_name[-1:] == "s" ):
				str_go = "go off"
		
		desc_ways_out += "%s %s to the " % ( str_name, str_go )
			
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
	lat, long = OSMUtilities.latlong_for_data( node_in )
	out = "%s (%2.8f,%2.8f).\n" % ( AdventureUtilities.description_for_way( way_in, True ), lat, long )
	out += "You are standing %s.\n" % desc_ways
	out += desc_ways_out
	
	if( DebugUtilities.get_debugmode() ):
		# describe things
		rel = osm_connector.NodeRelations( id )
		print "relationships: %s" % rel
	
	return out, ways_out