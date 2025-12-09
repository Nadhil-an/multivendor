from django.shortcuts import render,redirect
from vendor.models import Vendor
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from accounts.models import User


def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['long']
        return lng, lat
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('long')
        request.session['lat'] = lat
        request.session['long'] = lng
        return lng, lat
    else:
        return None


def home(request):

    # If vendor → redirect to vendor dashboard
    if request.user.is_authenticated and request.user.role == User.RESTAURANT:
        return redirect('vendorhome')

    # If customer → allow them to view home.html (NO redirect needed)
    # So do NOT redirect customers

    location = get_or_set_current_location(request)

    if location is not None:
        lng, lat = location
        pnt = GEOSGeometry(f'POINT({lng} {lat})', srid=4326)
        
        vendors = Vendor.objects.filter(
            user_profile__location__distance_lte=(pnt, D(km=1000))
        ).annotate(
            distance=Distance("user_profile__location", pnt)
        ).order_by("distance")

        for v in vendors:
            v.km = round(v.distance.km, 1)
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]

    return render(request, 'home.html', {'vendors': vendors})

