from django.db import models
from master_data.models import Suppliers
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
    cov = models.IntegerField(blank=False, null=False, default=0)
    tanning = models.BooleanField(default=False)
    finishing = models.BooleanField(default=False)
    notes = models.TextField()
    flamability_status = models.IntegerField(choices=FLAMABILITY_STATUS, default=4)

    def __str__(self):
        return self.description

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


#class ForbiddenHazStat(models.Model):
 #   id_hs=models.ForeignKey(HazardStatements, null=False, on_delete = models.CASCADE)



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
    id_chemical=models.ForeignKey(Chemicals, null=False, on_delete = models.CASCADE)
    sds = models.CharField(max_length=255, blank=False, null=False)
    rev_date = models.DateField()
    conformityReach = models.BooleanField(default=True)
    reg_id=models.ForeignKey(RegReach, null=False, on_delete = models.CASCADE)


class ChemicalHazardStatements(models.Model):
    id_chemical=models.ForeignKey(Chemicals, null=False, on_delete = models.CASCADE)
    id_sds=models.ForeignKey(Sds, null=False, on_delete = models.CASCADE)
    id_hs=models.ForeignKey(HazardStatements, null=False, on_delete = models.CASCADE)


