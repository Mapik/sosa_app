import dash_html_components as html
from utils import data_processing as dp
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import plotly.graph_objects as go
from config import config
import datetime as dt
from section import report_section as rs

def generate_section(pathname, data):
  section_name = pathname[1:]
  if section_name == 'overview':
    feature_dict_item = 'prod_year'
    one_dim_prod_year = dp.prepare_count(data, 
                                         feature_dict_item, 
                                         config.features_dict[feature_dict_item]['dppc_additional_filters_1'], 
                                         config.features_dict[feature_dict_item]['dppc_additional_filters_2'], 
                                         config.features_dict[feature_dict_item]['dppc_do_sorting'], 
                                         config.features_dict[feature_dict_item]['dppc_convert_to_string'],)
    feature_dict_item = 'version'
    one_dim_version = dp.prepare_count(data, 
                                         feature_dict_item, 
                                         config.features_dict[feature_dict_item]['dppc_additional_filters_1'], 
                                         config.features_dict[feature_dict_item]['dppc_additional_filters_2'], 
                                         config.features_dict[feature_dict_item]['dppc_do_sorting'], 
                                         config.features_dict[feature_dict_item]['dppc_convert_to_string'],)
    data['price_value_pln_brutto'] = round(data['price_value_pln_brutto'], -3)
    data['mileage'] = round(data['mileage'], -3)
    price_and_year = data[data['price_value_pln_brutto']<data['price_value_pln_brutto'].quantile(0.99)]
    price_and_version = price_and_year.sort_values('version')
    mileage_and_year = data[data['mileage']<data['mileage'].quantile(0.99)]
    mileage_and_version = mileage_and_year.sort_values('version')

    mileage_and_year_fig = px.box(mileage_and_year, x='prod_year', y='mileage')
    mileage_mean = mileage_and_year.groupby(['prod_year'])['mileage'].mean()
    mileage_mean = mileage_mean.reset_index()
    mileage_and_prod_year_mean = px.line(mileage_mean, x='prod_year', y='mileage')
    mileage_and_prod_year_mean.data[0].update(mode='markers+lines')
    mileage_and_year_fig.append_trace(mileage_and_prod_year_mean.data[0],None,None)

    mileage_and_version_fig = px.box(mileage_and_version, x='version', y='mileage')#, points='all', hover_name='index')
    mileage_mean = mileage_and_version.groupby(['version'])['mileage'].mean()
    mileage_mean = mileage_mean.reset_index()
    mileage_and_version_mean = px.line(mileage_mean, x='version', y='mileage')
    mileage_and_version_mean.data[0].update(mode='markers+lines')
    mileage_and_version_fig.append_trace(mileage_and_version_mean.data[0],None,None)
    full_section_layout = html.Div([
        html.Div(id='ss1', children=[html.H3('Filtry')]),
        html.Div(id='ss2', children=[html.H3('Ile aut pochodzi z danego rocznika?'),
                                     create_layout(one_dim_prod_year, 'prod_year')]),
        html.Div(id='ss3', children=[html.H3('Ile aut jest danej wersji?'),
                                     create_layout(one_dim_version, 'version')]),
        html.Div(id='ss4', children=[html.H3('Jaka jest srednia cena danego rocznika?'),
                                     html.Div([dcc.Graph(id='price_and_year', figure=px.box(price_and_year, x='prod_year', y='price_value_pln_brutto'))])]),
        html.Div(id='ss5', children=[html.H3('Jaka jest srednia cena wersji?'),
                                     html.Div([dcc.Graph(id='price_and_version', figure=px.box(price_and_version, x='version', y='price_value_pln_brutto'))])]),
        html.Div(id='ss6', children=[html.H3('Jaki jest sredni przebieg danego rocznika?'),
                                     html.Div([dcc.Graph(id='mileage_and_year', figure=mileage_and_year_fig)])]),
        html.Div(id='ss7', children=[html.H3('Jaki jest sredni przebig wersji?'),
                                     html.Div([dcc.Graph(id='mileage_and_version', figure=mileage_and_version_fig)])]),
        ])
  elif section_name == 'prod_year_version':
    full_section_layout = html.Div([
        html.Div(id='ss1', children=[html.H3('Filtry')]),
        html.Div(id='ss2', children=[html.H3('Rozkład cen w danym roczniku')]),
        html.Div(id='ss3', children=[html.H3('Rozkład przebiegów w danym roczniku')]),
        html.Div(id='ss4', children=[html.H3('Rozkład po latach produkcji')]),
        html.Div(id='ss5', children=[html.H3('Jakie silniki dominują?')]),
        html.Div(id='ss6', children=[html.H3('Co mają na wyposażeniu?')]),
        html.Div(id='ss7', children=[html.H3('Sctter plot - cena vs przebieg?')]),
        ])
  elif section_name == 'mileage_price':  
    full_section_layout = html.Div([
        html.Div(id='ss1', children=[html.H3('Filtry')]),
        html.Div(id='ss2', children=[html.H3('Wersje')]),
        html.Div(id='ss3', children=[html.H3('Roczniki')]),
        ])
  else:
    full_section_layout = html.Div([html.H4('Dane będą dostępne wkrótce. Zajrzyj do innej zakładki.')])
  return full_section_layout 


def create_layout(df_offer_from, section_name):
  print('{} - START chart 1'.format(dt.datetime.now()))
  return html.Div([dcc.Graph(
      id=section_name,
      figure=px.bar(df_offer_from, x=section_name, y="perc", barmode='stack')
  )])
