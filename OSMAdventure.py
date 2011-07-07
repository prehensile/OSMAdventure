import GeoUtilities
import OsmApi
import OSMUtilities
import math
import AdventureUtilities
import AdventureClient
from DebugUtilities import DebugUtilities
import IPInfoDB


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

def parse_way_out( fragment, ways_out ):
	out = None
	if( fragment in AdventureUtilities.verbose_cardinals ):
		fragment = AdventureUtilities.verbose_cardinals[ fragment ]
	if( fragment in ways_out ):
		# part is a cardinal and we have a way for it
		out = ways_out[ fragment ]
	return( out )

osm_connector = OsmApi.OsmApi()
next_node, next_way = OSMUtilities.get_nearest_node_to_latlong( osm_connector, lat, long )

# game loop
while( next_node ):
	
	desc, ways_out = AdventureClient.go_to_node( osm_connector, next_node, next_way )
	print desc
	
	mode_input = True
	while( mode_input ):
		input = None
		while( input is None ):
			input = raw_input(">")
		
		# parse input
		parts = input.split(" ")
		command = parts[ 0 ]
		parsed = parse_way_out( command, ways_out )
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
					print "You feel your skin prickle and a sense of apprehension, as in the moment before a long-gathering storm breaks. The feeling gathers in intensity until, just at the point you feel like you're ready to scream, it snaps off and you realise that you're not standing *anywhere*. Your mouth, if you could be sure of having one at this point, would be full of the taste of tin."
					print "A tiny, brisk voice says 'please wait for the next available operator' and muzak begins to play where you imagine the base of your skull would be."
					next_node, next_way = OSMUtilities.get_nearest_node_to_latlong( osm_connector, tlat, tlon )
					if( next_node and next_way ):
						mode_input = False
					else:
						print "I couldn't find a suitable landing spot near that location. Sorry!"
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
				parsed = parse_way_out( part, ways_out )
				if( parsed ):
					next_node, next_way = parsed
					mode_input = False
			else:
				print "I don't know how to %s." % command
				input = False

print "OSMAdventure finished normally"				
		
		
	