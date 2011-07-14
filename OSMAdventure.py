import GeoUtilities
import OsmApi
import OSMUtilities
import math
import AdventureUtilities
import IPInfoDB
import math
from sets import Set
from DebugUtilities import DebugUtilities
from AdventureUtilities import AdventureWay

def parse_way_out( fragment, ways_out ):
	out = None
	if( fragment in AdventureUtilities.verbose_cardinals ):
		fragment = AdventureUtilities.verbose_cardinals[ fragment ]
	if( fragment in ways_out ):
		# part is a cardinal and we have a way for it
		out = ways_out[ fragment ]
	return( out )

def go_to_node( osm_connector, node_in, way_in  ):
	
	# get OSM way data associated with this node
	node_id = OSMUtilities.id_for_data( node_in )
	ways_in = osm_connector.NodeWays( node_id )
	
	## working dictionaries
	# each key is the name of a way out, each entry a list of ways associated with that name
	ways_out = {} 	
	# each key is an OSM highway type, each entry a count of those types. used to disambiguate unnamed ways 
	unnamed_types = {}
	
	# step through ways_in
	for way_data in ways_in:
		
		# create a new instance of complex object
		way = AdventureWay( way_data )
		way_name = None
		
		# get way_name (used as key in ways_out)
		if( way.is_unnamed() ):
			# count unnamed ways
			num_types = 0
			way_type = way.highway_type
			if( way_type in unnamed_types ):
				num_types = unnamed_types[ way_type ] 
			unnamed_types[ way_type ] = num_types
			way_name = AdventureUtilities.description_for_way( way, num_types )
			num_types += 1
		else:
			way_name = way.get_name()
		
		# add way to list in ways_out
		ways = None
		if( way_name in ways_out ):
			ways = ways_out[ way_name ]
		else:
			ways = []
		ways.append( way )
		ways_out[ way_name ] = ways
	
	return ways_out

## 
# main

# baker street
lat = 51.522
long = -0.157

# rushmore road
#lat = 51.55464
#long = -0.05068

# dynamic lat / long
# ipinfo = IPInfoDB.get_info( "31.64.140.162" )
# lat = float( ipinfo[8] )
# long = float( ipinfo[9] )
# print( ipinfo[6] )

osm_connector = OsmApi.OsmApi()
next_node, next_way_data = OSMUtilities.get_nearest_node_to_latlong( osm_connector, lat, long )
next_way = AdventureWay( next_way_data )

# game loop
while( next_node ):
	
	# get ways out
	ways_out = go_to_node( osm_connector, next_node, next_way )
	
	# construct description
	lat, long = OSMUtilities.latlong_for_data( next_node )
	scratch_string = AdventureUtilities.description_for_way( next_way )
	if( next_way.is_unnamed() ):
		article = AdventureUtilities.indefinite_article( scratch_string )
		scratch_string = "%s %s" % ( AdventureUtilities.ucfirst( article ), scratch_string )
	desc_out = "%s (%2.8f,%2.8f).\n" % ( scratch_string, lat, long )
	desc_out += "You are standing"
	desc_ways_out = ""
	
	# construct cardinal directions out & describe
	bearing_next = -1
	bearing_prev = -1
	neighbour_prev = None
	neighbour_next	 = None
	directions_out = {}
	names_out = []
	names = ways_out.keys()
	name_out = None
	desc_name_out =  None
	for name in names:
		
		way_list = ways_out[ name ]
		cardinal_list = []
		name_out = name
		desc_name_out = name
		
		for way in way_list:
			
			if( way.is_unnamed() ):
				name_out = "The %s" % name
				desc_name_out = "%s %s" % (AdventureUtilities.indefinite_article( name ), name )
			
			neighbour_prev, neighbour_next = AdventureUtilities.get_neighbours( osm_connector, next_node, way )
			
			if( neighbour_next ):
				bearing_next = OSMUtilities.node_bearing( next_node, neighbour_next )
				cardinal_next = AdventureUtilities.cardinal_for_bearing( bearing_next )
				directions_out[ cardinal_next ] = ( neighbour_next, way )
				cardinal_list.append( AdventureUtilities.cardinal_descriptions[ cardinal_next ] )
			
			if( neighbour_prev ):
				bearing_prev = OSMUtilities.node_bearing( next_node, neighbour_prev )
				cardinal_prev = AdventureUtilities.cardinal_for_bearing( bearing_prev )
				directions_out[ cardinal_prev ] = ( neighbour_prev, way )
				cardinal_list.append( AdventureUtilities.cardinal_descriptions[ cardinal_prev ] )
				
		desc_ways_out += "%s %s to the %s.\n" % ( name_out, 
			AdventureUtilities.present_simple( name_out ),
			AdventureUtilities.join_list_verbose( cardinal_list ) )
		names_out.append( desc_name_out )
		
	# display description
	if( len( names_out ) > 1 ):
		desc_out += " at the junction of %s." % AdventureUtilities.join_list_verbose( names_out )
	else:
		desc_out += " on %s." %  AdventureUtilities.description_for_way( next_way )
	print desc_out
	print desc_ways_out
	
	# print directions_out
	
	# input mode go!
	mode_input = True
	while( mode_input ):
		input = None
		while( input is None ):
			input = raw_input("> ")
		
		# parse input
		parts = input.split(" ")
		command = parts[ 0 ]
		parsed = parse_way_out( command, directions_out )
		if( parsed ):
			next_node, next_way = parsed
			mode_input = False
		else:
			# command is more complex
			
			if( command == "teleport" ):
				if( len(parts) == 2 ):
					tlat, tlon = parts[1].split(",")
				elif( len(parts) == 3 ):
					tlat = parts[1]
					tlon = parts[2]
				print tlat
				print tlon
				if( tlat and tlon ):
					tlat = float(tlat)
					tlon = float(tlon)
					AdventureUtilities.render_template( "teleport_in" )
					next_node, next_way = OSMUtilities.get_nearest_node_to_latlong( osm_connector, tlat, tlon )
					if( next_node and next_way ):
						mode_input = False
					else:
						AdventureUtilities.render_template( "teleport_error" )
						input = False
						command = "look"
			elif( command == "look" ):
				print desc
				input = False
			elif( command == "quit" ):
				exit()
			elif( command == "exit" ):
				exit()
			elif( command == "bye" ):
				exit()
			elif( command == "logout" ):
				exit()
			elif( command == "debug" ):
				dbm = DebugUtilities.toggle_debugmode()
				if( dbm ):
					print "Debug mode is ON"
				else:
					print "Debug mode is OFF"
				input = False	
			elif( len(parts) == 2 ):
				# if the user typed anything followed by a cardinal, assume they want to go there
				part = parts[1]
				parsed = parse_way_out( part, directions_out )
				if( parsed ):
					next_node, next_way = parsed
					mode_input = False
			else:
				print "I don't know how to %s." % command
				input = False

print "OSMAdventure finished normally"				
		
		
	