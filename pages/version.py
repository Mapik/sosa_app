import dash_html_components as html
from utils import data_processing as dp
import pandas as pd
import plotly.express as px
import dash_core_components as dcc

def create_layout(df_version):
  return html.Div([dcc.Graph(
      id='version',
      figure={
          'data': [
              {'x': df_version['version'], 'y': df_version['N'], 'type': 'bar', 'name': 'version'},
          ],
          'layout': {
              'title': 'Wersje'
          }
      }
  )],className="page",)
