from django.db import models
from master_data.models import Suppliers
import datetime
from django.db.models import Count, Max, Subquery, OuterRef
# Create your models here.

FLAMABILITY_STATUS = (
    (1, "A - LIQUIDI MOLTO INFIAMMABILI"),
    (2, "B - LIQUIDI INFIAMMABILI"),
    (3, "C - LIQUIDI COMBUSTIBILI"),
    (4, "NON INFIAMMABILI")
)

DEPARTMENTS = (
    (1, "Bagnato"),
    (2, "Rifinizione")
)

class Chemicals(models.Model):
    id_chemical = models.AutoField(primary_key=True)
    id_supplier = models.ForeignKey(Suppliers, null=True, on_delete = models.CASCADE)
    description = models.CharField(max_length=50, blank=False, null=False)
    cov = models.DecimalField(max_digits=6, decimal_places=2,blank=False, null=False, default=0)
    tanning = models.BooleanField(default=False)
    finishing = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    flamability_status = models.IntegerField(choices=FLAMABILITY_STATUS, default=4)

    def __str__(self):
        return self.description

    '''Recupero l'ultimo prezzo del prodotto chimico'''  
    @property
    def get_price(self):
        price_object = Prices.objects.all()        
        
        print("price_object:" + str(price_object))
        partial_qs=price_object.values('id_chemical').annotate(latest_price=Max('price_date'))
    
        for parqs in partial_qs:
            if str(parqs['id_chemical'])==1:
                print("parqschemical: " + str(parqs['id_chemical']))
                print("parqschemical: " + str(parqs['latest_price']))

        price_object=price_object.filter(price_date__in=partial_qs.values('latest_price').order_by('-price_date')).get(id_chemical=self.id_chemical)
        #price_object=price_object.filter(price_date__in=partial_qs.values('latest_price').order_by('-price_date'))
        for priobj in price_object:
            print("ULTIMO:" + str(priobj["price_date"]))

        price = price_object.price        
        return price 

    '''Recupero l'ultima revisione della SDS'''
    def get_sds(self):
        sds_object = Sds.objects.all()        
        partial_qs=sds_object.values('id_chemical').annotate(latest_rev=Max('rev_date'))
        sds_object=sds_object.filter(rev_date__in=partial_qs.values('latest_rev').order_by('-rev_date')).get(id_chemical=self.id_chemical)             
        return sds_object 

    

    class Meta:
        verbose_name = "chemical"
        verbose_name_plural = "chemicals"

    




class Operations(models.Model):
    id_operation = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50, blank=False, null=False)
    order = models.IntegerField(blank=False, null=False, default=0)
    department = models.IntegerField(choices=DEPARTMENTS, default=1)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "operation"
        verbose_name_plural = "operations"

class Svhc(models.Model):
    id_svhc = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    numEc = models.CharField(max_length=50, blank=True, null=True)
    numCas = models.CharField(max_length=50, blank=True, null=True)
    inclusionDate = models.DateField(blank=True, null=True)
    inclusionReason = models.TextField()
    numDecision = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "svhc"
        verbose_name_plural = "svhc substances"

class PrecautionaryStatements(models.Model):
    id_ps = models.AutoField(primary_key=True)
    ps_code = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return 'Code {} precautionary Statement {}'. format(self.ps_code, self.description)

    class Meta:
        verbose_name = "precautionary statement"
        verbose_name_plural = "precautionary statements"


class HazardStatements(models.Model):
    id_hs = models.AutoField(primary_key=True)
    hs_code = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=50, blank=False, null=False)
    forbidden = models.BooleanField(default=False)

    def __str__(self):
        return 'Code {} hazard Statement {}'. format(self.hs_code, self.description)

    class Meta:
        verbose_name = "hazard statement"
        verbose_name_plural = "hazard statements"


class ChemicalsPackagingType(models.Model):
    id_packaging_type = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50, blank=False, null=False)
    kg = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.description

class ChemicalsPackaging(models.Model):
    id_chemical=models.ForeignKey(Chemicals, null=False, on_delete = models.CASCADE)
    id_packaging_type = models.ForeignKey(ChemicalsPackagingType, null=False, on_delete = models.CASCADE)


class RegReach(models.Model):
    reg_id = models.AutoField(primary_key=True)
    reg_name = models.CharField(max_length=50, blank=False, null=False)
    validity=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reg_name


class Sds(models.Model):
    id_sds = models.AutoField(primary_key=True)
    id_chemical=models.ForeignKey(Chemicals, blank=False, null=False, on_delete = models.CASCADE)
    sds = models.FileField(upload_to='sds')
    rev_date = models.DateField(blank=True, null=True)
    conformityReach = models.BooleanField(default=True)
    reg_id=models.ForeignKey(RegReach, null=False, on_delete = models.CASCADE)

        
    
class ChemicalHazardStatements(models.Model):
    id_chemical=models.ForeignKey(Chemicals, null=False, on_delete = models.CASCADE)
    id_sds=models.ForeignKey(Sds, null=False, on_delete = models.CASCADE)
    id_hs=models.ForeignKey(HazardStatements, null=False, on_delete = models.CASCADE)


class DangerSymbols(models.Model):
    id_danger = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50, blank=False, null=False)
    acronym = models.CharField(max_length=50, blank=False, null=False)
    symbol = models.ImageField(upload_to='danger_symbols')

    def __str__(self):
        return self.description

class ChemicalDangerSymbols(models.Model):
    '''XR Danger Symbols-Chemicals'''
    id_chemical=models.ForeignKey(Chemicals, null=False, on_delete = models.CASCADE)
    id_sds=models.ForeignKey(Sds, null=False, on_delete = models.CASCADE)
    id_danger=models.ForeignKey(DangerSymbols, null=False, on_delete = models.CASCADE)
    
    class Meta:
        unique_together=['id_sds', 'id_danger']



class DangersCategory(models.Model):
    '''Fields of dangers'''
    id_category=models.AutoField(primary_key=True)
    description=models.CharField(max_length=50, blank=False, null=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
    

class ChemicalsPrecautionaryStatement(models.Model):
    id_chemical=models.ForeignKey(Chemicals, null=False, on_delete = models.CASCADE)
    id_sds=models.ForeignKey(Sds, null=False, on_delete = models.CASCADE)
    id_ps=models.ForeignKey(PrecautionaryStatements, null=False, on_delete = models.CASCADE)


class Substances(models.Model):
    id_substance=models.AutoField(primary_key=True)
    description=models.CharField(max_length=255, blank=False, null=False)
    ec_number=models.CharField(max_length=50, blank=False, null=False)
    cas_number=models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Substance"
        verbose_name_plural = "Substances"

class ChemicalsSubstances(models.Model):
    '''XR substances - chemicals'''
    id_chemical=models.ForeignKey(Chemicals, null=False, on_delete = models.CASCADE)
    id_sds=models.ForeignKey(Sds, null=False, on_delete = models.CASCADE)
    id_substance=models.ForeignKey(Substances, null=False, on_delete = models.CASCADE)
    concentration=models.CharField(max_length=50, blank=False, null=False)


class PricesManager(models.Manager):
    '''Al momento non serve'''
    def max_of_prices(self, idc):
        qs=Prices.objects.all()    
        prova=qs.values('id_chemical').annotate(latest_price=Max('price_date'))
        qs=qs.filter(price_date__in=prova.values('latest_price').order_by('-price_date')).filter(**{'id_chemical':idc})
        return qs
    
    

class Prices(models.Model):
    id_chemical=models.ForeignKey(Chemicals, null=False, on_delete = models.CASCADE, related_name='prezzo')
    price=models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    price_date=models.DateField(default=datetime.date.today, blank=True, null=True)
    objects = PricesManager()  


'''funzione per numerare automaticamente il campo numero ordine
    Da integrare con il filtro data per anno
'''
def get_max_order_number() -> int:
        max_found = ChemicalOrder.objects.aggregate(Max('n_order'))["n_order__max"]
        if max_found is None:
            return 1
        return max_found + 1

class ChemicalOrder(models.Model):
    id_order= models.AutoField(primary_key=True)
    n_order = models.PositiveIntegerField(default=get_max_order_number)
    id_supplier = models.ForeignKey(Suppliers, null=True, on_delete = models.CASCADE)
    order_date = models.DateField(default=datetime.date.today)
    delivery_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user_id = models.IntegerField()
    conformity = models.BooleanField()
    n_conformity = models.BooleanField()
    n_conformity_reasons = models.TextField(blank=True, null=True)
    operator = models.CharField(max_length=50, blank=True, null=True)
    id_dich_int = models.IntegerField(blank=True, null=True)

    @property
    def days_open(self):
        days = (datetime.datetime.now().date()-self.order_date).days        
        return (days)
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    
    

    def __str__(self):
        return 'Ordine n. {} del {} fornitore {}'. format(self.n_order, self.order_date, self.id_supplier)

class ChemicalOrderDetail(models.Model):
    id_detail = models.AutoField(primary_key=True)
    id_order=models.ForeignKey(ChemicalOrder, on_delete = models.CASCADE)
    id_chemical=models.ForeignKey(Chemicals, on_delete = models.CASCADE)
    um=models.CharField(max_length=3)
    quantity=models.FloatField()
    id_packaging_type=models.ForeignKey(ChemicalsPackagingType, on_delete = models.DO_NOTHING)

    
    
    