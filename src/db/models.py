from django.db import models
from django.core.validators import FileExtensionValidator
import os
import pandas as pd


# Create your models here.
def content_file_name(instance, filename):
    if os.path.exists("database/db.sql"):
        os.remove("database/db.sql")
    Database.objects.all().delete()
    filename = 'db.sql'
    return os.path.join('database', filename)


class Database(models.Model):
    db = models.FileField(
        upload_to=content_file_name,
        blank=True,
        help_text="Choose SQL File",
        validators=[FileExtensionValidator(allowed_extensions=['sql'])])

    def __str__(self):
        return 'db.sql'
