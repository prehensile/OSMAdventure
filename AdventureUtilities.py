import OSMUtilities
import math
import random
import re
from random import choice
from DebugUtilities import DebugUtilities

cardinal_n = "n"
cardinal_ne = "ne"
cardinal_e = "e"
cardinal_se = "se"
cardinal_s = "s"
cardinal_sw = "sw"
cardinal_w = "w"
cardinal_nw = "nw"

verbose_cardinal_n = "north"
verbose_cardinal_ne = "north-east"
verbose_cardinal_e = "east"
verbose_cardinal_se = "south-east"
verbose_cardinal_s = "south"
verbose_cardinal_sw = "south-west"
verbose_cardinal_w = "west"
verbose_cardinal_nw = "north-west"

verbose_cardinals = { 	verbose_cardinal_n: cardinal_n, verbose_cardinal_ne: cardinal_ne,
						verbose_cardinal_e: cardinal_e, verbose_cardinal_se: cardinal_se,
						verbose_cardinal_s: cardinal_s, verbose_cardinal_sw: cardinal_sw,
						verbose_cardinal_w: cardinal_w, verbose_cardinal_nw: cardinal_nw }

cardinal_descriptions = { 	cardinal_n: verbose_cardinal_n, cardinal_ne: verbose_cardinal_ne,
							cardinal_e: verbose_cardinal_e, cardinal_se: verbose_cardinal_se,
							cardinal_s: verbose_cardinal_s, cardinal_sw: verbose_cardinal_sw,
							cardinal_w: verbose_cardinal_w, cardinal_nw: verbose_cardinal_nw }

unnamed_strings = [	"anonymous", "mysterious", "unnamed",
					"nameless", "unidentified", "unknown" ]

def ucfirst( word ):
	return "%s%s" % ( word[:1].upper(), word[1:] )

def indefinite_article( noun ):
	if( noun[-1:].lower() == "s" ):
		return "some"
	elif( re.match( "[aeiou]", noun.lower() ) ):
		return "an"
	else:
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
		if( DebugUtilities.get_debugmode() ):
			print way
		highway = "highway"
		if( tag and OSMUtilities.key_highway in tag ):
			highway = tag[ OSMUtilities.key_highway ]
		if( is_title ):
			u_str = choice( unnamed_strings )
			name = "%s %s" % ( u_str, highway )
		else: 
			name = highway
	
		article = "the"
		if( definite_article is False ):
			article = indefinite_article( name )
		name = "%s %s" % (article, name)
		if( is_title ):
			name = ucfirst( name )
	
	return( name )

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