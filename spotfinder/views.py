from django.http import HttpResponse
from journeyDestinationDjango.settings import FOURSQ_CLIENT_ID, FOURSQ_CLIENT_SECRET
#from django.core import serializers
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
import foursquare
import threading
import Queue

# Create your views here.
@csrf_exempt
def index(request):
    """
    Show up the Google maps form here
    """
    try:
        points = request.POST['points']
        distanceLimit = request.POST['distanceLimit']
    except Exception as e:
        #points = '["52.706347,10.442505","52.513714,13.353676"]'
        print "There is an error in getting the post arguments: " + str(e)
        return HttpResponse("Wrong POST arguments")
    finally:
        print points

    try:
        client = foursquare.Foursquare(access_token=request.session['access_token'])
    except:
        client = foursquare.Foursquare(client_id=FOURSQ_CLIENT_ID, client_secret=FOURSQ_CLIENT_SECRET)

    #Parse the points
    points = simplejson.loads(points)

    #TWEAK THIS later!
    #more infos here: https://developer.foursquare.com/docs/venues/explore
    defaultParams = {'radius': float(min(distanceLimit, 100000)), 'section': 'topPicks', 'limit': 100, 'venuePhotos': 0}
    venues = []
    vids = []

    for point in points:
        defaultParams['ll'] = point
        venuesJson = client.venues.explore(params=defaultParams)
        venue = getMostInterestingPoint(venuesJson, 2)
        vid = venue[u'venue']['id']
        if venue and vid not in vids:
            venues.append(venue)
            vids.append(vid)

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

class AsyncCall(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue, returnArray, client):
        threading.Thread.__init__(self)
        self.queue = queue
        self.client = client
        self.returnArray = returnArray
    def run(self):
        while True:
            p = self.queue.get()

            venuesJson = self.client.venues.explore(params=p)
            venue = getMostInterestingPoint(venuesJson, 2)
            if venue:
                self.returnArray.append(venue)
            self.queue.task_done()
