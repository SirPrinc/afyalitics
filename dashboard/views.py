from django.shortcuts import render
import openpyxl
from .models import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import base64
from django.shortcuts import render
import pandas as pd
import seaborn as sns
import geopandas as gpd
import os
from django.conf import settings


# Create your views here.
def home(request):
    return render(request,'index.html')

def tables(request):
    data = AEFIRecords.objects.all()
    context = {"data":data}
    return render(request,"tables.html",context)

def export(request):
    return render(request,"export.html")

def plot_adr_reports(request):
    # Fetch data from the database
    data = pd.DataFrame(list(AEFIRecords.objects.values('Date_of_report', 'Reporter_state_or_province', 'Sex', 'Created_by_organisation_level_2')))
    
    month_df = data['Date_of_report'].value_counts().reset_index()
    month_df.columns = ['Month', 'Count']
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Count', y='Month', data=month_df, color="#304245")
    plt.xlabel('Number of Reports')
    plt.ylabel('Month')
    plt.title('ADR Reports by Month')
    plt.savefig('core/static/assets/images/adr_by_month.png')
    plt.close()

    # Slide 2: ADR Reports by Regions
    province_group_by = data.groupby('Reporter_state_or_province').size().reset_index(name='total_count')
    province_group_by = province_group_by.sort_values(by='total_count', ascending=False)
    grand_total = pd.DataFrame({'Reporter_state_or_province': ['Grand Total'], 'total_count': [province_group_by['total_count'].sum()]})
    plt.figure(figsize=(10, 6))
    sns.barplot(x='total_count', y='Reporter_state_or_province', data=province_group_by, color="#304245")
    plt.xlabel("")
    plt.ylabel("")
    plt.savefig('core/static/assets/images/region_distribution.png')
    plt.close()

    # Slide 3: Plotting a Map of ADR Reports by Regions
    tanzania_map = gpd.read_file("core/static/assets/shapefiles/tza_admbnda_adm1_20181019/tza_admbnda_adm1_20181019.shp")
    tanzania_map = tanzania_map.merge(province_group_by, left_on='ADM1_EN', right_on='Reporter_state_or_province')
    projected_crs = 'EPSG:32737'
    tanzania_map = tanzania_map.to_crs(projected_crs)
    plt.figure(figsize=(10, 10))
    ax = tanzania_map.plot(column='total_count', cmap='Blues', edgecolor='black')
    for x, y, label in zip(tanzania_map.geometry.centroid.x, tanzania_map.geometry.centroid.y, tanzania_map['Reporter_state_or_province']):
        ax.text(x, y, label, fontsize=8)
    plt.savefig('core/static/assets/images/map_region.png')
    plt.close()

    # Slide 5: ADR Reports in Regions by Gender
    region_sex_data = data.groupby(['Reporter_state_or_province', 'Sex']).size().reset_index(name='n')
    region_sex_data = region_sex_data.assign(total=region_sex_data.groupby('Reporter_state_or_province')['n'].transform('sum'))
    region_sex_data_sorted = region_sex_data.sort_values(by='total', ascending=True)
    region_sex_pivot_sorted = region_sex_data_sorted.pivot(index='Reporter_state_or_province', columns='Sex', values='n').fillna(0)
    region_sex_pivot_sorted.plot(kind='bar', stacked=True, color=['#2887c8', '#66c992'], figsize=(10, 6))
    plt.xticks(rotation=90)
    plt.xlabel('')
    plt.ylabel('')
    plt.title('')
    plt.legend(title='Sex', loc="best")
    plt.savefig('core/static/assets/images/region_sex_distribution.png')
    plt.close()

    # Pie Chart for Summary of Gender Report
    sex_data_new = data['Sex'].value_counts(normalize=True).reset_index()
    sex_data_new.columns = ['Sex', 'perc']
    sex_data_new['labels'] = (sex_data_new['perc'] * 100).astype(int).astype(str) + '%'
    plt.figure(figsize=(8, 8))
    plt.pie(sex_data_new['perc'], labels=sex_data_new['labels'], colors=['#003a6c', '#363636', 'white'], autopct='%1.1f%%', startangle=140)
    plt.title('')
    plt.savefig('core/static/assets/images/sex_data_new.png')
    plt.close()

    # Slide 7: ADR Reports by TMDA Zones
    tmda_zones = data['Created_by_organisation_level_2'].value_counts().reset_index()
    tmda_zones.columns = ['Var1', 'Freq']
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Var1', y='Freq', data=tmda_zones, color="#304245", order=tmda_zones.sort_values('Freq', ascending=False)['Var1'])
    for index, row in tmda_zones.iterrows():
        plt.text(row.name, row.Freq, row.Freq, color='black', ha="center", va="bottom", size=8)
    plt.gca().set_facecolor('white')
    plt.xticks(rotation=70, verticalalignment='top', ma="right")
    plt.gca().tick_params(axis='y', which='both', left=False, labelleft=False)
    plt.xlabel('')
    plt.ylabel('')
    plt.savefig('core/static/assets/images/tmda_zones.png')
    plt.close()

    # Render the template
    return render(request, 'dashboard.html')


def plot_view(request):
    plt.figure(figsize=(5, 3))
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.savefig('core/static/assets/images/plot.png')
    plt.close()

    return render(request, 'dashboard.html')

















