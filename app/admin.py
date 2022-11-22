from django.contrib import admin
from .models import User, FundApplication, Department

# Register your models here.

admin.site.register(User)
admin.site.register(FundApplication)
admin.site.register(Department)
