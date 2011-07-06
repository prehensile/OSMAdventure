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

# game loop
next_node = current_node
next_way = current_way
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
		if( command in ways_out ):
			# command is a cardinal and we have a way for it
			next_node, next_way = ways_out[ command ]
			mode_input = False
		else:
			# command is more complex
			
			# if the user typed something followed by a cardinal, assume they want to go there
			if( len(parts) == 2 ):
				part = parts[1]
				if( part in ways_out ):
					# part is a cardinal and we have a way for it
					next_node, next_way = ways_out[ part ]
					mode_input = False
			
			elif( command == "quit" ):
				exit()
			elif( command == "exit" ):
				exit()
			elif( command == "bye" ):
				exit()
			elif( command == "logout" ):
				exit()
			
			if( mode_input ):
				print "I don't know how to %s." % command

print "OSMAdventure finished normally"				
		
		
	