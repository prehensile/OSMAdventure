class DebugUtilities:
	
	_debugmode = False
	@staticmethod
	def get_debugmode():
		return( DebugUtilities._debugmode )
	@staticmethod
	def set_debugmode( db_in ):
		DebugUtilities._debugmode = db_in
		return( DebugUtilities._debugmode )
	@staticmethod
	def toggle_debugmode():
		db = DebugUtilities.get_debugmode()
		if( db ):
			db = False
		else:
			db = True
		return( DebugUtilities.set_debugmode( db ) )
		
	@staticmethod
	def log( msg ):
		if( DebugUtilities._debugMode ):
			print msg