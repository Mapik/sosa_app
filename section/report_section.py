import dash_html_components as html
from utils import data_processing as dp
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import plotly.graph_objects as go
from config import config
import datetime as dt

def generate_section(pathname, data):
  # NIE DZIAŁA OVERVIEW
  # TRZEBA PRZEJRZEĆ SEKCJA PO SEKCJI
  print('{} - START generate_section - data preparation'.format(dt.datetime.now()))
  pathname = pathname[1:]
  section_name = map_link_to_section_name(pathname)
  sections = [params['feature_name'] for href, params in config.section_items_dict.items()]
  if section_name == 'overview':
    full_section_layout = html.Div([html.H4('Dane będą dostępne wkrótce. Zajrzyj do innej zakładki.')])
  else:
      if section_name == 'prod_year':
        df_one_dim = dp.prepare_count(data, section_name, config.section_items_dict[pathname]['dppc_additional_filters_1'], config.section_items_dict[pathname]['dppc_additional_filters_2'], config.section_items_dict[pathname]['dppc_do_sorting'], config.section_items_dict[pathname]['dppc_convert_to_string'],)
        full_section_layout = create_layout(df_one_dim, section_name)
      elif section_name == 'fuel_type':
        df_one_dim = dp.prepare_count(data, section_name, config.section_items_dict[pathname]['dppc_additional_filters_1'], config.section_items_dict[pathname]['dppc_additional_filters_2'], config.section_items_dict[pathname]['dppc_do_sorting'], config.section_items_dict[pathname]['dppc_convert_to_string'],)
        full_section_layout = create_layout(df_one_dim, section_name)
      elif section_name == 'mileage':
        df_one_dim = dp.prepare_bins_one_dim(data, section_name)
        full_section_layout = create_layout(df_one_dim, section_name)
      elif section_name == 'price_value_pln_brutto':
        df_one_dim = dp.prepare_bins_one_dim(data, section_name)
        full_section_layout = create_layout(df_one_dim, section_name)
      elif section_name in sections:
        #one dimensional
        df_one_dim = dp.prepare_count(data, section_name, config.section_items_dict[pathname]['dppc_additional_filters_1'], config.section_items_dict[pathname]['dppc_additional_filters_2'], config.section_items_dict[pathname]['dppc_do_sorting'], config.section_items_dict[pathname]['dppc_convert_to_string'],)
        #vs year and price
        df_vs_price_and_year = dp.vs_price_and_year(data, section_name)
        #vs fuel type
        df_vs_fuel_type = dp.vs_fuel_type(data, section_name)
        #vs mileage 
        df_vs_mileage = dp.vs_mileage(data, section_name)
        print('{} - END generate_section - data preparation'.format(dt.datetime.now()))
        print('{} - START generate_section - chart preparation'.format(dt.datetime.now()))
        full_section_layout = full_layout(df_one_dim, df_vs_price_and_year, df_vs_fuel_type, df_vs_mileage, section_name)
        print('{} - END generate_section - chart preparation'.format(dt.datetime.now()))
      else:
        full_section_layout = html.Div([html.H4('Dane będą dostępne wkrótce. Zajrzyj do innej zakładki.')])
  return full_section_layout 

def create_layout(df_offer_from, section_name):
  print('{} - START chart 1'.format(dt.datetime.now()))
  return html.Div([dcc.Graph(
      id='offer-from',
      figure=px.bar(df_offer_from, x=section_name, y="perc", barmode='stack')
  )],
  className="page",)

def create_one_dim_chart(data, section_name):
  print('{} - START chart onedim'.format(dt.datetime.now()))
  return html.Div([dcc.Graph(
      id='offer-from',
      figure={'data':[{
          'x':data[section_name],
          'y':data['perc'],
          'mode':'bar'}],
              'layout':{'clickmode': 'event+select'}}
  )],
  className="page",)

def create_one_dim_chart2(data, section_name):
  print('{} - START chart onedim'.format(dt.datetime.now()))
  return html.Div([dcc.Graph(
      id='offer-from',
      figure=go.Figure(
        data = [go.Bar(x=data[section_name], y=data['perc'])],
        layout_clickmode = 'event+select'
        )
  )],
  className="page",)
  
def create_layout2(df_offer_from2, section_name):
  print('{} - START chart 2'.format(dt.datetime.now()))
  return html.Div([dcc.Graph(
      id='offer-from2',
      figure=px.bar(df_offer_from2, x="prod_year", y="price_value_pln_brutto", color=section_name, barmode='group').update(layout={'clickmode':'event+select'})
  )],
  className="page",)
  
def create_layout3(df_offer_from3, section_name):
  print('{} - START chart 3'.format(dt.datetime.now()))
  fig = px.bar(df_offer_from3, x=section_name, y="N", color='fuel_type', barmode='stack')
  fig.layout.clickmode = 'event+select'
  return html.Div([dcc.Graph(
      id='offer-from3',
      figure=fig
  )],
  className="page",)

def create_layout4(df_offer_from4, section_name):
  print('{} - START chart 4'.format(dt.datetime.now()))
  return html.Div([dcc.Graph(
      id='offer-from4',
      figure = px.bar(df_offer_from4, x="mileage_bins", y="N", color=section_name, barmode="group")
  )],
  className="page",)

def full_layout(df_offer_from, df_offer_from2, df_offer_from3, df_offer_from4, section_name):
  return html.Div([
      create_layout(df_offer_from, section_name),
      create_layout2(df_offer_from2, section_name),
      create_layout3(df_offer_from3, section_name),
      create_layout4(df_offer_from4, section_name),
      ]
      )


def map_link_to_section_name(pathname):
  if pathname == '' or pathname == '/overview':
    section = 'overview'
  else:
    #pathname = pathname[1:]
    section = config.section_items_dict[pathname]['feature_name']
  return section


