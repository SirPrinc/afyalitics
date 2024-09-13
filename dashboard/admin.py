from django.contrib import admin

from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class AEFIRecordsAdmin(ImportExportModelAdmin):
    list_display = ['Sex','Reporter_state_or_province','Date_of_report','Created_by_organisation_level_2']

admin.site.register(AEFIRecords,AEFIRecordsAdmin)
