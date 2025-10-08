import uuid
from django.conf import settings
from django.db import models

from useraccount.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Property(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    title=models.CharField(max_length=255)
    description=models.TextField()
    price_per_day=models.IntegerField()
    cabins=models.IntegerField()
    bathrooms=models.IntegerField()
    guests=models.IntegerField()
    country=models.CharField(max_length=255)
    country_code=models.CharField(max_length=10)
    category=models.CharField(max_length=255)
    #favorite
    favoritess = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='favorites_properties',blank=True)
    ##
    image=CloudinaryField('image')
    host=models.ForeignKey(User,related_name='properties',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def image_url(self):
        url = str(self.image.url)
        if url.startswith('http'):
            return url  # Cloudinary (already full URL)
        return f'{settings.WEBSITE_URL}{url}'

    
class Reservation(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    property= models.ForeignKey(Property, related_name='reservations', on_delete=models.CASCADE)
    start_date= models.DateField()
    end_date= models.DateField()
    number_of_days = models.IntegerField()
    guests = models.IntegerField()
    total_price= models.FloatField()
    created_by= models.ForeignKey(User, related_name='reservations',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
