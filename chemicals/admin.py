from django.contrib import admin
from .models import (
    Chemicals, Operations, Svhc, 
    PrecautionaryStatements, HazardStatements, Prices, 
    RegReach, Sds, DangerSymbols,
    ChemicalOrder, ChemicalOrderDetail,ChemicalsPackagingType,
    Substances,

    )
                    
class ChemicalsPackagingTypeModelAdmin(admin.ModelAdmin):
    model = ChemicalsPackagingType
    list_display = ["description", "kg"]
    search_fields = ["description"]


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
    list_display = ["id_chemical", "price", "price_date"]
    search_fields = ["price_date"]

class RegReachModelAdmin(admin.ModelAdmin):
    model = RegReach
    list_display = ["reg_id", "reg_name", "validity"]
    
class SdsModelAdmin(admin.ModelAdmin):
    model = Sds
    list_display = ["id_sds", "id_chemical", "sds", "rev_date", "conformityReach", "reg_id"]
    

class DangerSymbolsModelAdmin(admin.ModelAdmin):
    model = DangerSymbols
    list_display = [
        "id_danger", 
        "description", 
        "acronym", 
        "symbol",         
        ]

class ChemicalOrderModelAdmin(admin.ModelAdmin):
    model = ChemicalOrder
    list_display = [
        "id_order", 
        "n_order", 
        "id_supplier", 
        "order_date",         
        "delivery_date",
        ]
    search_fields = ["n_order"]


class ChemicalOrderDetailModelAdmin(admin.ModelAdmin):
    model = ChemicalOrderDetail
    list_display = [
        "id_detail", 
        "id_order", 
        "id_chemical", 
        "um",         
        "quantity",
        ]
    search_fields = ["id_order"]

class SubstancesModelAdmin(admin.ModelAdmin):
    model = Substances
    list_display = [
        "id_substance",
        "description",
        "cas_number",
        "ec_number"
    ]
    search_fields = ["cas_number"]


admin.site.register(Chemicals, ChemicalsModelAdmin)
admin.site.register(Operations, OperationsModelAdmin)
admin.site.register(Svhc, SvhcModelAdmin)
admin.site.register(PrecautionaryStatements, PrecautionaryStatementsModelAdmin)
admin.site.register(HazardStatements, HazardStatementsModelAdmin)
admin.site.register(Prices, PricesModelAdmin)
admin.site.register(RegReach, RegReachModelAdmin)
admin.site.register(Sds, SdsModelAdmin)
admin.site.register(DangerSymbols, DangerSymbolsModelAdmin)
admin.site.register(ChemicalOrder, ChemicalOrderModelAdmin)
admin.site.register(ChemicalOrderDetail, ChemicalOrderDetailModelAdmin)
admin.site.register(ChemicalsPackagingType, ChemicalsPackagingTypeModelAdmin)
admin.site.register(Substances, SubstancesModelAdmin)



    
