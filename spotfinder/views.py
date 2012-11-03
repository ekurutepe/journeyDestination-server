from django.http import HttpResponse
import journeyDestinationDjango.settings
# Create your views here.
def index(request):
    """
    Show up the Google maps form here
    """
    try:
        points = request.POST['points']
    except:
        return HttpResponse("Dont call me without points")
    try:
        client = foursquare.Foursquare(access_token=request.POST['apiToken'])
    except:
        client = foursquare.Foursquare(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')

    #Parse the points

    for point in points:
        client.venues.explore("{},{}".format

    return HttpResponse("Insert Google Maps Source and Destination here")


#api call:
#https://api.foursquare.com/v2/venues/explore
