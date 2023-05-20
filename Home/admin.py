from django.contrib import admin
from .models import Meds,Users,Expiry
# Register your models here.
admin.site.register(Meds)
admin.site.register(Users)
admin.site.register(Expiry)