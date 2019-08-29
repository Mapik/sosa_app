import dash_html_components as html
from utils import data_processing as dp
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import plotly.graph_objects as go

def create_layout(df_offer_from):
  return html.Div([dcc.Graph(
      id='offer-from',
      figure={
          'data': [
              {'x': df_offer_from['offer_from'], 'y': df_offer_from['N'], 'type': 'bar', 'name': 'N Offer from'},
          ],
          'layout': {
              'title': 'Offer from'
          }
      }
  )],
  className="page",)

def create_layout2(df_offer_from2):
  return html.Div([dcc.Graph(
      id='offer-from2',
      figure=px.line(df_offer_from2, x="prod_year", y="price_value_pln_brutto", color="offer_from")
  )],
  className="page",)
  
def create_layout3(df_offer_from3):
  return html.Div([dcc.Graph(
      id='offer-from3',
      figure=px.bar(df_offer_from3, x="offer_from", y="N", color='fuel_type', barmode='stack')
  )],
  className="page",)
  
def full_layout(df_offer_from, df_offer_from2, df_offer_from3):
  return html.Div([
      create_layout(df_offer_from),
      create_layout2(df_offer_from2),
      create_layout3(df_offer_from3),
      ]
      )