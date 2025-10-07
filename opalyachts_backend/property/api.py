# use the serializers to make the url available for front

from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from .forms import PropertyForm
from .models import Property, Reservation
from .serializers import PropertiesListSerializer,PropertiesDetailSerializer, ReservationsListSerializer
from useraccount.models import User

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    #auth
    try:
        token=request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
        token = AccessToken(token)
        user_id=token.payload['user_id']
        user=User.objects.get(pk=user_id)
    except Exception as e:
        user=None
        
    
    #

    favorites=[]
    properties=Property.objects.all()

    #for Search
    country=request.GET.get('country','')
    category=request.GET.get('category','')
    checkin_date=request.GET.get('checkIn','')
    checkout_date=request.GET.get('checkOut','')
    cabins=request.GET.get('numCabins','')
    guests=request.GET.get('numGuests','')
    bathrooms=request.GET.get('numBathrooms','')

    #filter per landlord
    landlord_id = request.GET.get('landlord_id', '')
    if landlord_id:
        properties=properties.filter(host=landlord_id)

    is_favorites= request.GET.get('is_favorites','')
    if is_favorites:
        properties=properties.filter(favoritess__in=[user])

    #for Search    
    if guests:
        properties=properties.filter(guests__gte=guests)
    if cabins:
        properties=properties.filter(cabins__gte=cabins)
    if bathrooms:
        properties=properties.filter(bathrooms__gte=bathrooms)
    if country:
        properties=properties.filter(country=country)
    if category and category!='undefined':
        properties=properties.filter(category=category)
    
    if checkin_date and checkout_date:
        exact_matches= Reservation.objects.filter(start_date=checkin_date) | Reservation.objects.filter(end_date=checkout_date)
        overlap_matches= Reservation.objects.filter(start_date__lte=checkout_date, end_date__gte=checkin_date)
        all_matches = []

        for reservation in exact_matches | overlap_matches:
            all_matches.append(reservation.property_id)
        properties = properties.exclude(id__in=all_matches)
   
    #Favorites

    if user:
        for property in properties:
            if user in property.favoritess.all():
                favorites.append(property.id)
    

    #
    serializer = PropertiesListSerializer(properties, many=True)

    return JsonResponse({
        'data':serializer.data,
        'favorites': favorites
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_reservations(request,pk):
    property=Property.objects.get(pk=pk)
    reservations= property.reservations.all()
    serializer=ReservationsListSerializer(reservations, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST','FILES'])
def create_property(request):
    form= PropertyForm(request.POST, request.FILES)
    
    if form.is_valid():
        property = form.save(commit=False)
        property.host = request.user
        property.save()

        return JsonResponse({'success': True})
    else:
        print('error', form.errors,form.non_field_errors)
        return JsonResponse({'erros': form.errors.as_json()}, status=400)
    
#api endpoint for showing yacht details

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_details(request,pk):
    property= Property.objects.get(pk=pk)
    serializer = PropertiesDetailSerializer(property, many=False)
    return JsonResponse(serializer.data)

@api_view(['POST'])
def book_property(request, pk):
    try:
        start_date=request.POST.get('start_date','')
        end_date=request.POST.get('end_date','')
        number_of_days=request.POST.get('number_of_days','')
        total_price=request.POST.get('total_price','')
        guests=request.POST.get('guests','')

        property=Property.objects.get(pk=pk)

        Reservation.objects.create(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_days=number_of_days,
            total_price=total_price,
            guests=guests,
            created_by=request.user
        )
        return JsonResponse({'success': True})

    except Exception as e:
        print('error', e)
        return JsonResponse({'success':False})


@api_view(['POST'])
def toggle_favorite(request,pk):
    try:
        prop = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return JsonResponse({'error': 'Property not found'}, status=404)

    user = request.user
    if user in prop.favoritess.all():   # ✅ use the correct field name
        prop.favoritess.remove(user)
        return JsonResponse({'is_favorite': False})
    else:
        prop.favoritess.add(user)
        return JsonResponse({'is_favorite': True})