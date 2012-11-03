from django.http import HttpResponse
from journeyDestinationDjango.settings import FOURSQ_CLIENT_ID, FOURSQ_CLIENT_SECRET
#from django.core import serializers
from django.utils import simplejson
import foursquare

# Create your views here.
def index(request):
    """
    Show up the Google maps form here
    """
    output = []
    try:
        points = request.POST['points']
    except:
        #return HttpResponse("Dont call me without points")
        output.append("Be careful. We are working with test values!<br>\n")
        points = '["52.706347,10.442505","52.513714,13.353676"]'
    try:
        client = foursquare.Foursquare(access_token=request.POST['apiToken'])
    except:
        client = foursquare.Foursquare(client_id=FOURSQ_CLIENT_ID, client_secret=FOURSQ_CLIENT_SECRET)

    #Parse the points
    points = simplejson.loads(points)

    #TWEAK THIS later!
    #more infos here: https://developer.foursquare.com/docs/venues/explore
    defaultParams = {'radius': 10000.0, 'section': 'topPicks', 'limit': 1000, 'venuePhotos': 0}
    venues = []
    for point in points:
        defaultParams['ll'] = point
        venuesJson = client.venues.explore(params=defaultParams)
        venue = getMostInterestingPoint(venuesJson, 2)
        if venue:
            venues.append(venue)

    return HttpResponse(simplejson.dumps(venues), content_type="application/json")


#api call:
#https://api.foursquare.com/v2/venues/explore


def getMostInterestingPoint(venuesJson, minVal):
    """Return the dictionary of the highest rated point if it exceeds minVal"""
    highestVenue = None
    for venue in venuesJson[u'groups'][0]['items']:
        checkIns = venue[u'venue'][u'stats'][u'checkinsCount']
        if checkIns > minVal:
            if not highestVenue or highestVenue[u'venue'][u'stats'][u'checkinsCount'] < checkIns:
                highestVenue = venue
    return highestVenue
