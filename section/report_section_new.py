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
  pathname = pathname[1:]
  section_name = rs.map_link_to_section_name(pathname)
  sections = [params['feature_name'] for href, params in config.section_items_dict.items()]
  if section_name == 'overview':
    full_section_layout = html.Div([
        html.Div(id='ss1', children=[html.H3('subsection 1')]),
        html.Div(id='ss2', children=[html.H3('subsection 2')]),
        html.Div(id='ss3', children=[html.H3('subsection 3')]),
        ])
  else:
      if section_name == 'prod_year':
        full_section_layout = html.Div([
            html.Div(id='ss1', children=[html.H3('subsection 1')]),
            html.Div(id='ss2', children=[html.H3('subsection 2')]),
            html.Div(id='ss3', children=[html.H3('subsection 3')]),
            ])
      elif section_name == 'fuel_type':
        full_section_layout = html.Div([
            html.Div(id='ss1', children=[html.H3('subsection 1')]),
            html.Div(id='ss2', children=[html.H3('subsection 2')]),
            html.Div(id='ss3', children=[html.H3('subsection 3')]),
            ])
      elif section_name == 'mileage':
        full_section_layout = html.Div([
            html.Div(id='ss1', children=[html.H3('subsection 1')]),
            html.Div(id='ss2', children=[html.H3('subsection 2')]),
            html.Div(id='ss3', children=[html.H3('subsection 3')]),
            ])
      elif section_name == 'price_value_pln_brutto':
        full_section_layout = html.Div([
            html.Div(id='ss1', children=[html.H3('subsection 1')]),
            html.Div(id='ss2', children=[html.H3('subsection 2')]),
            html.Div(id='ss3', children=[html.H3('subsection 3')]),
            ])
      elif section_name in sections:
        full_section_layout = html.Div([
            html.Div(id='ss1', children=[html.H3('subsection 1')]),
            html.Div(id='ss2', children=[html.H3('subsection 2')]),
            html.Div(id='ss3', children=[html.H3('subsection 3')]),
            ])
      else:
        full_section_layout = html.Div([
            html.Div(id='ss1', children=[html.H3('subsection 1')]),
            html.Div(id='ss2', children=[html.H3('subsection 2')]),
            html.Div(id='ss3', children=[html.H3('subsection 3')]),
            ])
  return full_section_layout 
