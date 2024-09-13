from django.db import models

# Create your models here.

class AEFIRecords(models.Model):
    Sex = models.CharField(max_length=200)
    Reporter_state_or_province = models.CharField(max_length=200)
    Date_of_report = models.DateField(max_length=200)
    Created_by_organisation_level_2 = models.CharField(max_length=200)

    def __str__(self):
        field_names = [field.name for field in self._meta.fields if field.name != 'id']
        field_values = [f"{field}: {getattr(self, field)}" for field in field_names]
        return ", ".join(field_values)
