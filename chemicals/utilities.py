
'''Pezzo di codice per organizzare (p.e.) le schede di sicurezza in cartelle
    con il nome del fornitore
    preso dal link
    https://stackoverflow.com/questions/60808408/django-rest-framework-is-it-possible-to-organize-uploaded-files-by-associated-u
'''
import os
from django.conf import settings
from django.db import models

# Create user dir if non-existant and return upload path
def upload_path(instance, filename):
    path = os.path.join(settings.MEDIA_ROOT, str(instance.user))
    if not os.path.isdir:
        os.mkdir(path)

    return os.path.join(path, filename)


class MyMail(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    attachment = models.FileField(upload_to=upload_path)
    
    
'''Fine upload'''