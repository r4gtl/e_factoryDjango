from django.contrib import admin
from .models import Suppliers, VatCodes

# Register your models here.
admin.site.register(Suppliers)
admin.site.register(VatCodes)