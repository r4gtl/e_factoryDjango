from django.db import models

# Create your models here.
class Suppliers(models.Model):
    id_supplier = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100, blank=False, null=False)
    vat_number = models.CharField(max_length=11)
    cf_number = models.CharField(max_length=16)
    address = models.CharField(max_length=100)
    cap = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100)
    prov = models.CharField(max_length=10)
    country_state = models.CharField(max_length=10, null=True, blank=True)
    gg_valuta = models.IntegerField(blank=True, null=True)
    sds_path = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #standard data
    vat_perc = models.ForeignKey('VatCodes', on_delete=models.CASCADE,  blank=True, null=True)

    class Meta:
        verbose_name = "supplier"
        verbose_name_plural = "suppliers"
        
    def __str__(self):
        return self.company_name

    
class VatCodes(models.Model):
    vat_code = models.CharField(max_length=3, blank=False, null=False, primary_key=True)
    description = models.CharField(max_length=10)
    tax_perc = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Vat Code"
        verbose_name_plural = "Vat Codes"
