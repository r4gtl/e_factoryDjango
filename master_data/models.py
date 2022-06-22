from django.db import models
from django.urls import reverse


# Create your models here.

class SuppliersCategories(models.Model):
    category = models.CharField(max_length=50, blank=False, null=False)
    note = models.TextField()
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.category



class Suppliers(models.Model):
    id_supplier = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100, blank=False, null=False)
    vat_number = models.CharField(max_length=11, unique=True)
    cf_number = models.CharField(max_length=16, blank=True)
    address = models.CharField(max_length=100, blank=True)
    cap = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    prov = models.CharField(max_length=10, blank=True)
    country_state = models.CharField(max_length=10, null=True, blank=True)
    gg_valuta = models.IntegerField(blank=True, null=True)
    sds_path = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(SuppliersCategories, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #standard data
    vat_perc = models.ForeignKey('VatCodes', on_delete=models.DO_NOTHING,  blank=True, null=True)

    
        
    def __str__(self):
        return self.company_name
    
    def get_absolute_url(self):
        return reverse("master_data:update-supplier", kwargs={"pk": self.id_supplier})
    
    class Meta:
        verbose_name = "supplier"
        verbose_name_plural = "suppliers"

class SuppliersContacts(models.Model):
    contact_name=models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    id_supplier = models.ForeignKey(Suppliers, null=True, on_delete = models.CASCADE)

    def get_absolute_url(self):
        return reverse("update-contact", kwargs={"pk": self.pk})
    
class VatCodes(models.Model):
    vat_code = models.CharField(max_length=3, blank=False, null=False, primary_key=True)
    description = models.CharField(max_length=10, blank=True)
    tax_perc = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Vat Code"
        verbose_name_plural = "Vat Codes"


        
class Customers(models.Model):
    company_name = models.CharField(max_length=100, blank=False, null=False)
    vat_number = models.CharField(max_length=11, unique=True)
    cf_number = models.CharField(max_length=16, blank=True)
    address = models.CharField(max_length=100, blank=True)
    cap = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    prov = models.CharField(max_length=10, blank=True)
    country_state = models.CharField(max_length=10, null=True, blank=True)            
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #standard data
    vat_perc = models.ForeignKey('VatCodes', on_delete=models.DO_NOTHING,  blank=True, null=True)
    
    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"


class CustomersContacts(models.Model):
    contact_name=models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    customer = models.ForeignKey(Suppliers, null=True, on_delete = models.CASCADE)

    # def get_absolute_url(self):        
    #     return reverse("update-contact", kwargs={"pk": self.pk})