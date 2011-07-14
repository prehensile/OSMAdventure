import OSMUtilities
from OSMUtilities import OSMNode
import math
import random
import re
from random import choice
from DebugUtilities import DebugUtilities
import os.path

def ucfirst( word ):
	return "%s%s" % ( word[:1].upper(), word[1:] )

def indefinite_article( noun ):
	if( noun[-1:].lower() == "s" ):
		return "some"
	elif( re.match( "[aeiou]", noun.lower() ) ):
		return "an"
	else:
		return "a"

def present_simple( noun ):
	if( noun[-1:].lower() == "s" ):
		return "are"
	return "is"

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

def get_neighbours( osm_connector, node, way ):
	
	result = osm_connector.WayGet( way.get_id() )
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
	
def render_template( template_name ):
	fn = "templates/%s.txt" % template_name
	path = os.path.realpath(__file__)
	path = os.path.dirname( path )
	path = os.path.join( path, fn )
	fh = open( path )
	txt = fh.read()
	fh.close()
	print txt
	return( txt )


def description_for_way( way, type_count = 0 ):
	if( way.is_unnamed() ):
		
		highway_type = way.highway_type()
		unnamed_str = choice( unnamed_strings )
		
		if( type_count > 1 ):
			ordinal = ordinal_for_number( type_count )
			highway_type = "%s %s" %  ( ordinal, highway_type )
		
		return( "%s %s" % ( unnamed_str, highway_type ) )
		
	return( way.get_name() )


def join_list_verbose( items ):
	out = ""
	ln = len( items )
	i = 0
	for item in items:
		out += item
		if( i < ln-2 ):
			out += ", "
		elif( i < ln-1 ):
			out += " and "
		i += 1
	return( out )
	
def ordinal_for_number( num ):
	if( num < 10 ):
		return( one_ordinals[ num ] )
	elif( num < 20 ):
		return( teen_ordinals[ num-10 ] )
	else:
		tail = one_ordinals[ num%10 ]
		head = ten_cardinals[ int(num/10) ]
		return( "%s-%s" % ( tail, head ) )
	return( none )

class AdventureWay( OSMNode ):
	
	def is_unnamed( self ):
		return( self.get_name() is None )
	
	def highway_type( self ):
		if( self.tag and OSMUtilities.key_highway in self.tag ):
			return( self.tag[ OSMUtilities.key_highway ] )


##
# boring constants
			
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

one_ordinals = [ "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth" ]
teen_ordinals = [ "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth" ]
ten_cardinals = [ "ten", "twenty", "thirty", "fourty", "fifty", "sixty", "seventy", "eighty", "ninety" ]