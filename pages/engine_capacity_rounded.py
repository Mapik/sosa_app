import dash_html_components as html
from utils import data_processing as dp
import pandas as pd
import plotly.express as px
import dash_core_components as dcc


def create_layout(app, df_offer_from):
  return dcc.Graph(
      id='offer-from',
      figure={
          'data': [
              {'x': df_offer_from['offer_from'], 'y': df_offer_from['N'], 'type': 'bar', 'name': 'N Offer from'},
          ],
          'layout': {
              'title': 'Offer from'
          }
      }
  ),
