import pandas as pd
import numpy as np

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
  """Prepare onedimensional count"""
  count = df.groupby([column_name])['N'].count()
  count = count.reset_index()
  if additional_filters_1:
    count = count[count[column_name]!=0]
  if additional_filters_2:
    count = count[count['N']>=5]
  if do_sorting:
    count = count.sort_values('N', ascending = False)
    count = count.reset_index(drop=True)
  if convert_to_string:
    if column_name == 'engine_power':
      count[column_name] = count[column_name].map(str)+' KM'
    if column_name == 'engine_capacity_rounded':
      count[column_name] = 'poj. '+count[column_name].map(str)
  return count

def prepare_bins(df, column_name):
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

