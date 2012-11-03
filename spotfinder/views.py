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
    output = []
    print request.POST['points']

    try:
        points = request.POST['points']
    except Exception as e:
        return HttpResponse(str(e))
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

    #add to multi threading queue
    queue = Queue.Queue()
    #dont p
    for i in range(1): #more than 1 will give blocks from foursquare
        t = AsyncCall(queue, venues, client)
        t.setDaemon(True)
        t.start()

    for point in points:
        defaultParams['ll'] = point
        queue.put(defaultParams)

    queue.join()

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
