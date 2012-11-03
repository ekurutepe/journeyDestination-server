import httplib2
import urllib2

ll = (52.706347,10.442505)

h = httplib2.Http(".cache")
h.add_credentials('user', 'pass')
r, content = h.request("https://api.github.co://api.foursquare.com/v2/venues/explore", "GET")

print r['status']
print r['content-type']
