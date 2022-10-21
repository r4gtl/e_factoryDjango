from django.db import models


class Ward(models.Model):
    idreparto = models.AutoField(primary_key=True, db_column="idreparto")
    description = models.CharField(max_length=50, null=False, blank=False, help_text="Nome reparto", db_column="descrizionereparto")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["description"]
        verbose_name_plural = "wards"
        db_table = "reparti"

class Role(models.Model):
    idmansione = models.AutoField(primary_key=True, db_column="idmansione")
    description = models.CharField(max_length=50, null=False, blank=False, help_text="Nome mansione", db_column="descrizionemansione")
    idreparto = models.ForeignKey(Ward, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["description"]
        verbose_name_plural = "roles"
        db_table = "mansioni"

class HumanResource(models.Model):
    idpersona = models.AutoField(primary_key=True, db_column="idpersona")
    cognomedipendente = models.CharField(max_length=50, null=False, blank=False)
    nomedipendente = models.CharField(max_length=50, null=False, blank=False)
    dataassunzione = models.DateField(null=False, blank=False)
    datadimissioni = models.DateField(null=True, blank=True)
    idmansione = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    idreparto = models.ForeignKey(Ward, null=True, blank=True, on_delete=models.SET_NULL)
    qualifica = models.CharField(max_length=50, null=True, blank=True)
    commenti = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-dataassunzione"]
        verbose_name_plural = "dipendenti"
        db_table = "dipendenti"
