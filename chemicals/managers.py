from django.db import models
from django.db.models import Max, Prefetch,Count, Subquery,OuterRef

#===============================================ChemicalManager
class ChemicalQuerySet(models.QuerySet):
        pass


class ChemicalManager(models.Manager):
    
    def get_queryset(self):
        return ChemicalQuerySet(self.model, using=self._db)
    
    def get_latest_price(self):
        pass
#===============================================Fine ChemicalManager
    
#===============================================PriceManager

class PriceQuerySet(models.QuerySet):    
    def get_max_prices(self):
        latest_price=self.filter(
        price_date=Subquery(
            (self.filter
            (id_chemical=OuterRef('id_chemical'))
            .values('id_chemical')
            .annotate(last_price=Max('price_date'))
            .values('last_price')[:1]
        )
        )
    )
        return latest_price


class PriceManager(models.Manager):     
    def get_queryset(self):
        return PriceQuerySet(self.model, using=self._db)    
    
    def get_max_of_price(self): 
        return self.get_queryset().get_max_prices()
    
#===============================================Fine PriceManager

#===============================================SDSManager
class SDSQuerySet(models.QuerySet):    
    def get_max_sds(self):
        latest_rev=self.filter(
        rev_date=Subquery(
            (self.filter
            (id_chemical=OuterRef('id_chemical'))
            .values('id_chemical')
            .annotate(last_rev=Max('rev_date'))
            .values('last_rev')[:1]
        )
        )
    )
        return latest_rev


class SDSManager(models.Manager):     
    def get_queryset(self):
        return SDSQuerySet(self.model, using=self._db)    
    
    def get_max_of_sds(self): 
        return self.get_queryset().get_max_sds()
#===============================================Fine SDSManager