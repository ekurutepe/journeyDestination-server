from django.http import HttpResponse
# Create your views here.
def index(request):
    """
    Show up the Google maps form here
    """
    try:
        points = request.POST['points']
    except:
        return HttpResponse("Dont call me without points")

    for point in points:
        pass
    return HttpResponse("Insert Google Maps Source and Destination here")


#api call:
#https://api.foursquare.com/v2/venues/explore
