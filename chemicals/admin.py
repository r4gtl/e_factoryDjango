from django.contrib import admin
from .models import Chemicals, Operations, Svhc, PrecautionaryStatements, HazardStatements, Prices
                    

class ChemicalsModelAdmin(admin.ModelAdmin):
    model = Chemicals
    list_display = ["description", "id_supplier"]
    search_fields = ["description"]


class OperationsModelAdmin(admin.ModelAdmin):
    model = Operations
    list_display = ["description", "order", "department"]
    search_fields = ["description"]


class SvhcModelAdmin(admin.ModelAdmin):
    model = Svhc
    list_display = ["name"]
    search_fields = ["numEC", "numCas"]


class PrecautionaryStatementsModelAdmin(admin.ModelAdmin):
    model = PrecautionaryStatements
    list_display = ["ps_code", "description"]
    search_fields = ["ps_code"]


class HazardStatementsModelAdmin(admin.ModelAdmin):
    model = HazardStatements
    list_display = ["description"]
    search_fields = ["hs_code"]

class PricesModelAdmin(admin.ModelAdmin):
    model = Prices
    list_display = ["price"]
    search_fields = ["price_date"]



admin.site.register(Chemicals, ChemicalsModelAdmin)
admin.site.register(Operations, OperationsModelAdmin)
admin.site.register(Svhc, SvhcModelAdmin)
admin.site.register(PrecautionaryStatements, PrecautionaryStatementsModelAdmin)
admin.site.register(HazardStatements, HazardStatementsModelAdmin)
admin.site.register(Prices, PricesModelAdmin)



    
