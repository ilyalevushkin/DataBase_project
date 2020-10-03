from django.contrib import admin
from .models import *

admin.site.register([Virus,
                     Epidemiology,
                     PlaceOfBeating,
                     TransmissionWays,
                     Epidemic,
                     Period,
                     Place,
                     PlaceDemography,
                     Profile,
                     Favourites])
