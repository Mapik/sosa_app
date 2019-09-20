from utils import data_processing as dp
from utils import read_data
import pandas as pd
import numpy as np 
import matplotlib as mt
import matplotlib.pyplot as plt
import plotly.io as pio
pio.renderers.default = "browser"
import plotly.express as px
import math
import plotly.graph_objects as go
from section import report_section as rs
from config import config

math.ceil(34509)

def col_univariate_analysis(col_to_check):
    #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.boxplot.html
    #https://matplotlib.org/api/_as_gen/matplotlib.lines.Line2D.html
    #https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.boxplot.html
    #https://matplotlib.org/gallery/subplots_axes_and_figures/subplots_demo.html
    #https://stackoverflow.com/questions/20656663/matplotlib-pandas-error-using-histogram
    plt.figure()
    fig, (ax1, ax2) = plt.subplots(1,2)
    fig.suptitle('{} ({})'.format(col_to_check.name, col_to_check.dtype))
    hst = ax1.hist(col_to_check.dropna(), edgecolor = 'k')
    bxp = ax2.boxplot(col_to_check.dropna())
    plt.show()
    d = col_to_check.describe()
    stats_data = {'count': d[0],
                  'std': d[2], 
                  'min': d[3], 
                  'caps_low': bxp['caps'][0].get_ydata()[0],
                  '25%': d[4], 
                  '50%': d[5], 
                  'median': bxp['medians'][0].get_ydata()[0], 
                  'mean': d[1],
                  '75%': d[6], 
                  'caps_high': bxp['caps'][1].get_ydata()[0],
                  'whiskers': np.sort(bxp['whiskers'][0].get_ydata()), 
                  'fliers': np.sort(bxp['fliers'][0].get_ydata()), 
                  'n_fliers': pd.Series(bxp['fliers'][0].get_ydata()).count(),
                  'max': d[7]
                  }
    
    stats_df = pd.DataFrame.from_dict(data=stats_data, orient='index', columns=['stat_value'])
    #print(stats_df)
    return stats_df 

# jednowymiarowy
    
  
# vs cena i rocznik
# vs rodzaj silnika
# vs przebieg     

df = read_data.read_data_from_excel('vw', 'Passat')
dp.prepare_bins(df, 'mileage')
dp.prepare_count(df, 'offer_from')

# wyliczanie 99 kwantyla przebiegu i zaokąglanie go w górę, zeby uzyska ładną iloć binów

q99 = df['mileage'].quantile(0.99)
rounding = str(q99).find('.') - 1
denominator = int('1' + ''.join(['0'] * rounding))
q99_for_ceiling = q99/denominator
q99_ceil = math.ceil(q99_for_ceiling)
q99_r = q99_ceil * denominator
#q99_r = round(q99, -5)
n_bins = (q99_r/(denominator/5))+1
  
df = df[df['mileage']<q99_r]

# dzielenie przebiegu na biny

df['mileage_bins'] = pd.cut(df['mileage'], np.linspace(0, q99_r,n_bins))
df['mileage_bins'] = df.apply(lambda x: pd.Interval(x['mileage_bins'].left.astype(int), x['mileage_bins'].right.astype(int)), axis=1)
df['mileage_bins'].value_counts().sort_index().plot.bar()

# wykres pokazujący przebieg w podziale na offer_from w plotly - bar

grb = df.groupby(['mileage_bins', 'offer_from'])['N'].count().reset_index()
grb['mileage_bins'] = grb['mileage_bins'].astype(str)
fig = px.bar(grb, x="mileage_bins", y="N", color="offer_from", barmode="group")
fig.show()

# wykres pokazujący przebieg w podziale na offer_from w plotly - liniowy

grb = df.groupby(['mileage_bins', 'offer_from'])['N'].count().reset_index()
grb['mileage_bins'] = grb['mileage_bins'].astype(str)
trc_company = grb[grb['offer_from'] == 'Firmy']
trc_private = grb[grb['offer_from'] == 'Osoby prywatnej']
fig = px.bar(trc_company, x="mileage_bins", y="N")
fig.add_trace(
    go.Bar(
        x=trc_private['mileage_bins'],
        y=trc_private['N'],
        #mode="lines",
        #line=go.scatter.Line(color="gray"),
        showlegend=False)
)
fig.show()

# wykres pokazujący przebieg w podziale na offer_from w matplotlib

grb = df.groupby(['mileage_bins', 'offer_from'])['offer_from'].count().unstack('offer_from').fillna(0)
grb.plot(kind='bar', stacked=True)


# zamiana na procenty

df = read_data.read_data_from_excel('vw', 'Passat')
count = df.groupby(['offer_from'])['N'].count()

count = df['offer_from'].value_counts()
count = count.reset_index()
count['n_all'] = count['N'].sum()
count['perc']= round((count['N']/count['n_all'])*100,1)
count = count[['offer_from', 'perc']]

# pojedyncza seria na biny

df = read_data.read_data_from_excel('vw', 'Passat')

variable = df['price_value_pln_brutto']
q99 = variable.quantile(0.99)
rounding = str(q99).find('.') - 1
denominator = int('1' + ''.join(['0'] * rounding))
q99_for_ceiling = q99/denominator
q99_ceil = math.ceil(q99_for_ceiling)
q99_r = q99_ceil * denominator
n_bins = (q99_r/(denominator/5))+1

variable = variable[variable<q99_r]

# dzielenie przebiegu na biny

bins = pd.cut(variable, np.linspace(0, q99_r,n_bins))
bins = bins.apply(lambda x: pd.Interval(x.left.astype(int), x.right.astype(int)))
bins = bins.astype(str)

dp.prepare_count(df, 'price_value_pln_brutto')


# sprawdzenie dlaczego nie działa mielage

data = read_data.read_data_from_excel('vw', 'Passat')
data['mileage_bins'] = dp.prepare_bins(data['mileage'])
data['mileage'] = data['mileage_bins']
df_one_dim = dp.prepare_count(data, 'mileage')
figure=px.bar(df_one_dim, x='mileage', y="perc", barmode='stack')
figure.show()


# one-dim data dla ciaglych

data = read_data.read_data_from_excel('vw', 'Passat')
column_name = 'mileage'
bins = dp.prepare_bins(data[column_name])
grpb = bins.value_counts()
grpb = grpb.reset_index()
grpb = grpb.rename(columns={'index':column_name, 'mileage':'N'})
grpb = grpb.sort_values(column_name, ascending = True)
grpb[column_name] = grpb[column_name].astype('str')
grpb['n_all'] = grpb['N'].sum()
grpb['perc']= round((grpb['N']/grpb['n_all'])*100,1)
grpb = grpb[[column_name, 'perc']]


# cena

data = read_data.read_data_from_excel('vw', 'Passat')
column_name = 'price_value_pln_brutto'
df_one_dim = dp.prepare_bins_one_dim(data, column_name)

bins = dp.prepare_bins(data[column_name])
grpb = bins.value_counts()
grpb = grpb.reset_index()
grpb = grpb.rename(columns={'index':column_name, column_name:'N'})
grpb = grpb.sort_values(column_name, ascending = True)
grpb[column_name] = grpb[column_name].astype('str')
grpb['n_all'] = grpb['N'].sum()
grpb['perc']= round((grpb['N']/grpb['n_all'])*100,1)
grpb = grpb[[column_name, 'perc']]


#point and click

data = read_data.read_data_from_excel('vw', 'Passat')
section_name = 'version'
pathname = 'version'
df_one_dim = dp.prepare_count(data, section_name, config.section_items_dict[pathname]['dppc_additional_filters_1'], config.section_items_dict[pathname]['dppc_additional_filters_2'], config.section_items_dict[pathname]['dppc_do_sorting'], config.section_items_dict[pathname]['dppc_convert_to_string'],)
data = df_one_dim 

figure=go.Figure(
    data = [go.Bar(x=data[section_name], y=data['perc'])],
    layout_clickmode = 'event+select'
    )
figure.show()


{'data':[{
          'x':data[section_name],
          'y':'perc',
          'mode':'bar'}],
        'layout':{'clickmode': 'event+select'}}
figure.show()


# wyfiltrowanie aut

all_models = read_data.read_data_from_csv()
a = all_models.groupby(['maker', 'model'])['N'].count().sort_values(ascending = False).reset_index()
a = a[a['N']>=50]
makers = pd.Series(a['maker'].unique())
makers_list = []
for i in makers:
  makers_list.append({'label': i, 'value': i})
models_dict = {}  
for i in makers:
  models_dict[i] = []
  for model in a[a['maker']==i]['model']:
    models_dict[i].append({'label': model, 'value': model})

