from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="dashboard-index"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("importdata/",views.import_data,name="import-data"),
    path("tables/",views.tables,name="table-data"),
    path("export/",views.export,name="export-data-charts"),
]