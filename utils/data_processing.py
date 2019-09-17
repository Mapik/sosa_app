import pandas as pd
import numpy as np
import math 
import datetime as dt

def filter_data(df):
  df = df[[
      'maker',
      'model',
      'offer_from',
      'version',
      'prod_year',
      'engine_capacity_rounded',
      'engine_power',
      'fuel_type',
      'gearbox',
      'transmission_group',
      'color',
      'country_of_origin',
      'n_params_available',
      'n_features',
      'mileage',
      'price_value_pln_brutto']]
  df = df[df['maker']=='Volkswagen']
  df = df[df['model']=='Passat']
  return df

def prepare_count(df, 
                  column_name, 
                  additional_filters_1=False, 
                  additional_filters_2=False, 
                  do_sorting=False,
                  convert_to_string=False):
  """Prepare onedimensional count for categorical columns"""
  print('{} - START prepare_count'.format(dt.datetime.now()))
#  if column_name in ['price_value_pln_brutto','mileage']:
#    bins = prepare_bins(df[column_name])
#    df[column_name] = bins
  count = df.groupby([column_name])['N'].count()
  count = count.reset_index()
  count['n_all'] = count['N'].sum()
  count['perc']= round((count['N']/count['n_all'])*100,1)
  count = count[[column_name, 'perc']]
  if additional_filters_1: #odrzucam np. przypadki z 0 KM
    count = count[count[column_name]!=0]
  if additional_filters_2: #odrzucam dla czytelnosci jakies nieznaczace wartosci
    count = count[count['perc']>=0.5]
  if do_sorting: #sortowanie po wysokosci slupków
    count = count.sort_values('perc', ascending = True)
    count = count.reset_index(drop=True)
  if convert_to_string:
    if column_name == 'engine_power':
      count[column_name] = count[column_name].map(str)+' KM'
    if column_name == 'engine_capacity_rounded':
      count[column_name] = 'poj. '+count[column_name].map(str)
  print('{} - END prepare_count'.format(dt.datetime.now()))
  return count

def vs_price_and_year(df,
                      column_name):
  """Prepare data for chart with price and prod year"""
  pr_and_yr = df.groupby([column_name, 'prod_year'])['price_value_pln_brutto'].mean()
  pr_and_yr = pr_and_yr.reset_index()
  return pr_and_yr

def vs_fuel_type(df,
                 column_name):
  fuel_type = df.groupby([column_name, 'fuel_type'])['N'].count().reset_index()
  return fuel_type

def vs_mileage(df,
              column_name):
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
  
  grb = df.groupby(['mileage_bins', column_name])['N'].count().reset_index()
  grb['mileage_bins'] = grb['mileage_bins'].astype(str)
  
  return grb

def prepare_bins(variable):
  # variable - pd.Series
  # wyliczanie 99 kwantyla przebiegu i zaokąglanie go w górę, zeby uzyska ładną iloć binów
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
  #bins = bins.astype(str)
  return bins

def prepare_bins_one_dim(data, 
                         column_name):
  """One-dimensional count for continuos variables - milegae and price"""
  bins = prepare_bins(data[column_name])
  grpb = bins.value_counts()
  grpb = grpb.reset_index()
  grpb = grpb.rename(columns={'index':column_name, column_name:'N'})
  grpb = grpb.sort_values(column_name, ascending = True)
  grpb[column_name] = grpb[column_name].astype('str')
  grpb['n_all'] = grpb['N'].sum()
  grpb['perc']= round((grpb['N']/grpb['n_all'])*100,1)
  grpb = grpb[[column_name, 'perc']]
  return grpb

def prepare_bins_not_nice(df, column_name):
  bins_df = df[[column_name, 'N']]
  caps_low = bins_df[column_name].quantile(0.0)
  caps_high = bins_df[column_name].quantile(0.99)
  nbins = 10
  bins_df = bins_df[bins_df[column_name]<=caps_high]
  bins_df['bins'] = pd.cut(bins_df[column_name], bins = np.linspace(caps_low, caps_high, num = nbins))
  bins_df = prepare_count(bins_df, 'bins')
  #zaokraglenie intervalow i separator tysiaca
  bins_df['left'] = bins_df.apply(lambda x: x['bins'].left.round(), axis=1)
  bins_df['right'] = bins_df.apply(lambda x: x['bins'].right.round(), axis=1)
  bins_df['bins'] = bins_df['left'].map(str) + ' - ' + bins_df['right'].map(str)
  #formatowanie
  #https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html
  #https://pbpython.com/styling-pandas.html
  return bins_df[['bins', 'N']]

