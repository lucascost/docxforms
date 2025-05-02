import uuid
from django.db import models

from django.db import models

class Documento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    arquivo = models.FileField(upload_to='docs/')
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.arquivo.name