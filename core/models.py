from django.db import models
from accounts.models import User

class Bike(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    engine = models.CharField(max_length=100)
    mileage = models.CharField(max_length=100)
    transmission = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to="bikes/")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


class Comment(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField()
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.bike)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100)
    rentfor = models.IntegerField()
    time = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bike.name