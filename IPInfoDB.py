import urllib
import urllib2
import json

api_key = "e97c5b7634b39c5700d6fd4954b6cb85e8cf7355798afd95c295befa0a011ee3"
api_url = "http://api.ipinfodb.com/v3/ip-city/"

# OK;;31.64.140.162;UK;UNITED KINGDOM;ENGLAND;BRADFORD;-;53.788;-1.75;+00:00
def get_info( ip ):
	passdict = {"output":"raw", "key":api_key, "timezone": "false"  }
	if ip :
		try :
			passdict["ip"] = socket.gethostbyaddr(ip)[2][0]
		except : passdict["ip"] = ip
	urldata = urllib.urlencode(passdict)
	url = api_url + "?" + urldata
	urlobj = urllib2.urlopen(url)
	data = urlobj.read()
	urlobj.close()
	return data.split( ";" )