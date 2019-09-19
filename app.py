import pandas as pd
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from pages import (
    offer_from,
    version
)
from utils import read_data
from utils import data_processing as dp
from dash.exceptions import PreventUpdate
from section import report_section as rs
from config import config


#=======================
# Bootstrap
#=======================

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

#=======================
# Server
#=======================

app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

#=======================
# Data
#=======================

#vw_passat = read_data.read_data_from_excel('vw', 'Passat')
#toyota_avensis = read_data.read_data_from_excel('toyota', 'Avensis')
#ford_mondeo = read_data.read_data_from_excel('ford', 'Mondeo')
all_models = read_data.read_data_from_csv()

#=======================
# Define makers and models
#=======================

# wybranie dostępnych marek i modeli z pliku
# docelowo do zmiany - bez sensu, żeby za każdym razem to sprawdzać

a = all_models.groupby(['maker', 'model'])['N'].count().sort_values(ascending = False).reset_index()
a = a[a['N']>=50]
makers = pd.Series(a['maker'].unique()).sort_values()
makers_list = []
for i in makers:
  makers_list.append({'label': i, 'value': i})
models_dict = {}  
for i in makers:
  models_dict[i] = []
  for model in a[a['maker']==i]['model'].sort_values():
    models_dict[i].append({'label': model, 'value': model})


#=======================
# Config
#=======================

app.config.suppress_callback_exceptions = True
app.title = 'SOSA App'





#=======================
# index page
#=======================

index_page = html.Div([
      html.Div([
          html.Div([dcc.Dropdown(
           id='select-maker',
           options=makers_list,
#           [
#               {'label': 'VW', 'value': 'VW'},
#               {'label': 'Toyota', 'value': 'Toyota'},
#               {'label': 'Ford', 'value': 'Ford'}
#               ],
           value=None,
           placeholder = 'Wybierz producenta'
           ),], className='col-sm'),
          html.Div([dcc.Dropdown(
           id='select-model',
           options=[],
           value=None,
           placeholder = 'Wybierz model'
           ),], className='col-sm'),
          html.Div([
           dcc.Input(
              placeholder='Podaj adres e-mail...',
              type='text',
              value='',
              id='email',
              className='form-control'
              ),
             html.Small('Adres e-mail jest opcjonalny', className='text-muted')
              ], className='col-sm'),
          ], className='row form-group'),
      html.Div([
          html.Div([
              html.Button('Generuj raport', id='gen-report', className='btn btn-lg btn-outline-primary')
              ], className='col text-center')
          ],className='row form-group'),
      html.Div(id='report-div')
    ], className='container')

#=======================
# app.layout
#=======================
      
app.layout = html.Div([
  html.Div([
    html.Div([html.H1('SOSA App', className='display-4'), 
              html.P('Statystyki ofert sprzedaży aut', className='lead'),],
             className='container',),], 
    className='jumbotron jumbotron-fluid',
    style={'padding-top': '10px','padding-bottom': '10px'}),
  dcc.Location(id='url', refresh=False),
  index_page,
  dcc.Loading(id='loading-data',
              children=[html.Div(id='data-div', style={'display': 'none'})],
              type='circle')
])

#=======================
# section menu
#=======================

def generate_menu_items():
  html_ul = []
  for href, params in config.section_items_dict.items():
    class_value = 'nav-link'
    html_ul.append(html.Li([dcc.Link(params['menu_text'], href=href, className=class_value, id='nav-{}-btn'.format(href))], className='nav-item'),)
  return html_ul
  
nav1 = html.Div([
    html.Ul(generate_menu_items(), className='nav nav-pills justify-content-center')
    ])


#=======================
# callbacks
#=======================

#----------
# update model menu
#----------

@app.callback(
    Output(component_id='select-model', component_property='options'),
    [Input(component_id='select-maker', component_property='value')]
)
def update_models(maker):
    if maker is None:
        raise PreventUpdate
    elif maker is not None:
      return models_dict[maker]
#    elif maker == 'VW':
#      return [{'label': 'Passat', 'value': 'Passat'}]
#    elif maker == 'Toyota':
#      return [{'label': 'Avensis', 'value': 'Avensis'}]
#    elif maker == 'Ford':
#      return [{'label': 'Mondeo', 'value': 'Mondeo'}]
    else: 
        raise PreventUpdate

#----------
# update data div
#----------

@app.callback(
    Output(component_id='data-div', component_property='children'),
    [Input(component_id='gen-report', component_property='n_clicks')],
    [State(component_id='select-maker', component_property='value'),
     State(component_id='select-model', component_property='value')]
    )
def get_data(nclicks, maker, model):
  if model is None:
    raise PreventUpdate
  else:
    return None
#    df = read_data.read_data_from_excel(maker, model)
#    datasets = {
#         'df': df.to_json(orient='split', date_format='iso'),
#     }
#    return json.dumps(datasets)

#----------
# update report div
#----------

@app.callback(
    Output(component_id='report-div', component_property='children'),
    [Input(component_id='data-div', component_property='children'),],
    [State(component_id='select-maker', component_property='value'),
     State(component_id='select-model', component_property='value'),]
)
def generate_report(n_clicks, maker, model):
  if model is None:
    raise PreventUpdate
  else:
    report_page = html.Div([
        html.Div([html.H3('Wywietlam raport dla: {} {}'.format(maker, model)),]),
        html.Div([nav1]),
        dcc.Loading(id='loading-rep-section',
                    children=[html.Div(id='report-section')],
                    type='circle'),
#        html.Div(id='report-section'),
        ])
    return report_page

#----------
# update url when report is generated
#----------

@app.callback(
    Output('url', 'pathname'),
    [Input('report-div', 'children')]
    )
def update_url_aft_rep_gen(n_clicks):
  return '/overview'

#----------
# update section div
#----------

@app.callback(
    Output(component_id='report-section', component_property='children'),
    [Input(component_id='url', component_property='pathname'),
     Input(component_id='data-div', component_property='children')],
    [State(component_id='select-maker', component_property='value'),
     State(component_id='select-model', component_property='value'),]
)
def update_report_section(pathname, jsonified_cleaned_data, maker, model):
#  datasets = json.loads(jsonified_cleaned_data)
#  return rs.generate_section(pathname, pd.read_json(datasets['df'], orient='split'))
#  if model == "Avensis":
#    data = toyota_avensis
#  elif model == "Passat":
#    data = vw_passat
#  elif model == "Mondeo":
#    data = ford_mondeo
  data = all_models[all_models['model']==model]
  return rs.generate_section(pathname, data)
  
#----------
# update buttons pills
#----------

def generate_callbacks_outputs():
  outputs = []
  for href, text in config.section_items_dict.items():
    outputs.append(Output(component_id='nav-{}-btn'.format(href), component_property='className'))
  return outputs

@app.callback(
    generate_callbacks_outputs(),
    [Input(component_id='url', component_property='pathname')])
def update_nav_button_version(pathname):
  class_list = []
  #wygenerwanie 16 class
  for href, text in config.section_items_dict.items():
    if href in pathname:
      class_list.append('nav-link active')
    else:
      class_list.append('nav-link')
  return class_list
      
if __name__ == '__main__':
    app.run_server(debug=True)