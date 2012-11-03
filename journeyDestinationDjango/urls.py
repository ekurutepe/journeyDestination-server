from django.conf.urls import patterns, include, url
# from django.conf import settings
# # Uncomment the next two lines to enable the admin:
# # from django.contrib import admin
# # admin.autodiscover()

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'journeyDestinationDjango.views.home', name='home'),
#     # url(r'^journeyDestinationDjango/', include('journeyDestinationDjango.foo.urls')),

#     # Uncomment the admin/doc line below to enable admin documentation:
#     # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

#     # Uncomment the next line to enable the admin:
#     # url(r'^admin/', include(admin.site.urls)),



    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    


# )



urlpatterns = patterns('',
    # main page redirects to start or login
    url(r'^$', 'journeyDestinationDjango.foursq_auth.views.main', name='main'),
    # receive OAuth token from 4sq
    url(r'^callback/$', 'journeyDestinationDjango.foursq_auth.views.callback', name='oauth_return'),
    # # logout from the app
    url(r'^logout/$', 'journeyDestinationDjango.foursq_auth.views.unauth', name='oauth_unauth'),
    # # authenticate with 4sq using OAuth
    url(r'^auth/$', 'journeyDestinationDjango.foursq_auth.views.auth', name='oauth_auth'),
    # # main page once logged in
    url( r'^done/$', 'journeyDestinationDjango.foursq_auth.views.done', name='oauth_done' ),

    url(r'^searchVenues', include('spotfinder.urls')),

)

