from django.db import models
from django.db.models import Max, Prefetch,Count, Subquery,OuterRef


class ChemicalQuerySet(models.QuerySet):
        pass


class ChemicalManager(models.Manager):
    
    def get_queryset(self):
        return ChemicalQuerySet(self.model, using=self._db)
    
    def get_latest_price(self):
        pass
    
    

class PriceQuerySet(models.QuerySet):
    def get_max_prices(self, id_chemical):
        partial_qs=self.values('id_chemical').annotate(latest_price=Max('price_date'))
        price_object=self.filter(price_date__in=partial_qs.values('latest_price').filter(id_chemical=id_chemical).order_by('-price_date')).first()        
        return price_object.price
    # def get_max_prices(self):
    #     latest_price=self.objects.filter(
    #     price_date=Subquery(
    #         (self.objects.filter
    #         (id_chemical=OuterRef('id_chemical'))
    #         .values('id_chemical')
    #         .annotate(last_price=Max('price_date'))
    #         .values('last_price')[:1]
    #     )
    #     )
    # )
    #     return latest_price


class PriceManager(models.Manager):     
    def get_queryset(self):
        return PriceQuerySet(self.model, using=self._db)
    
    def get_max_of_price(self, id_chemical): 
        return self.get_queryset().get_max_prices(id_chemical)
    