import OSMUtilities
import math
import random
import re

cardinal_n = "n"
cardinal_ne = "ne"
cardinal_e = "e"
cardinal_se = "se"
cardinal_s = "s"
cardinal_sw = "sw"
cardinal_w = "w"
cardinal_nw = "nw"

cardinal_descriptions = { 	cardinal_n: "north", cardinal_ne: "north-east",
							cardinal_e: "east", cardinal_se: "south-east",
							cardinal_s: "south", cardinal_sw: "south-west",
							cardinal_w: "west", cardinal_nw: "north-west" }

unnamed_strings = [	"anonymous", "mysterious", "unnamed",
					"nameless", "unidentified", "unknown" ]

def indefinite_article( noun ):
	if( re.match( "[aeiou]", noun.lower() ) ):
		return "an"
	return "a"

def description_for_cardinal( cardinal ):
	return(  cardinal_descriptions[ cardinal ] )
	
def cardinal_for_bearing( bearing ):
	if( bearing < 0 ):
		bearing = math.pi + bearing
	out = ""
	inc = 0.125 * math.pi
	step = 0.25 * math.pi
	if( bearing < inc ):
		out = "n"
	elif( bearing < step + inc ):
		out = "ne"
	elif( bearing < (step*2) + inc ):
		out = "e"
	elif( bearing < (step*3) + inc ):
		out = "se"
	elif( bearing < (step*4) + inc ):
		out = "s"	
	elif( bearing < (step*5) + inc ):
		out = "sw"	
	elif( bearing < (step*6) + inc ):
		out = "w"
	elif( bearing < (step*7) + inc ):
		out = "nw"	
	elif( bearing < (step*8) ):
		out = "n"	
	return( out )	
		
	
def description_for_way( way, is_title = False, definite_article = False ):
	# print "description_for_way: %s" % way
	tag = OSMUtilities.tag_for_data( way )
	name = OSMUtilities.name_for_tag( tag )
	if( name is None ):
		print way
		highway = "highway"
		if( tag and OSMUtilities.key_highway in tag ):
			highway = tag[ OSMUtilities.key_highway ]
		if( is_title ):
			u_str = unnamed_strings[ int( len(unnamed_strings)-1 * random.random() ) ]
			name = "%s %s" % ( u_str, highway )
		else: 
			name = highway
	
		article = "the"
		if( definite_article is False ):
			article = indefinite_article( name )
		name = "%s %s" % (article, name)
		if( is_title ):
			name = name.capitalize()
	
	return( name )