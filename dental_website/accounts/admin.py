from django.contrib import admin
from .models import User,Patient,Staff
# Register your models here.

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Staff)

