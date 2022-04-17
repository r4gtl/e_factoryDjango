from django.contrib import admin
from .models import Suppliers, VatCodes, SuppliersCategories


class SupplierModelAdmin(admin.ModelAdmin):
    model = Suppliers
    list_display = ["company_name", "vat_number","cf_number", "address", "cap",
                    "city", "prov", "country_state", "category", "gg_valuta", "created_at", "updated_at"]
    search_fields = ["company_name", "vat_number"]
    list_filter = ["country_state", "vat_perc", "category"]

class VatCodesModelAdmin(admin.ModelAdmin):
    model = VatCodes
    list_display = ["vat_code", "description", "tax_perc"]
    search_fields = ["vat_code", "description"]

class SuppliersCategoriesModelAdmin(admin.ModelAdmin):
    model = SuppliersCategories
    list_display = ["category", "note"]
    search_fields = ["category"]

admin.site.register(Suppliers, SupplierModelAdmin)
admin.site.register(VatCodes, VatCodesModelAdmin)
admin.site.register(SuppliersCategories, SuppliersCategoriesModelAdmin)