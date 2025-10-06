#clean coding

from django.urls import path
from . import api

urlpatterns = [
    path('',api.properties_list,name='api_properties_list'),
    path('create/', api.create_property, name='api_create_property'),
    path('<uuid:pk>/',api.properties_details, name='api_properties_detail'),
    path('<uuid:pk>/book/', api.book_property,name='api_book_property'),
    path('<uuid:pk>/reservations/',api.properties_reservations,name='api_properties_reservations'),
    path('<uuid:pk>/toggle_favorite/',api.toggle_favorite,name='api_toggle_favorite'),

]
