from django.db import models

class Meds(models.Model):
    name = models.CharField(max_length=255)
    qty = models.IntegerField(default=0)
    perstrip = models.IntegerField(default=0)
    rtime = models.IntegerField(default=0)
    stkdays = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

    

class Users(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

class Expiry(models.Model):
    name = models.ForeignKey(to=Meds,on_delete=models.CASCADE)
    expiry = models.DateField()
    qty = models.IntegerField(default=0)