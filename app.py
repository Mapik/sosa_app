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

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

app.config.suppress_callback_exceptions = True
app.title = 'SOSA App'

index_page = html.Div([
#    html.Div([
#      html.Div([html.H1('SOSA App', className='display-4'), 
#                html.P('Statystyki ofert sprzedaży aut', className='lead'),],
#               className='container'),], 
#      className='jumbotron jumbotron-fluid'),
#    html.Div([
#      html.H1('SOSA App', className='display-4'), 
#      html.P('Statystyki ofert sprzedaży aut', className='lead'),
#      ], 
#      className='jumbotron'),
#    html.Div([
#      html.H1('SOSA App'), 
#      html.P('Statystyki ofert sprzedaży aut'),
#      ], 
#      className='page-header'),
      html.Div([
          html.Div([dcc.Dropdown(
           id='select-maker',
           options=[
               {'label': 'VW', 'value': 'VW'},
               {'label': 'Toyota', 'value': 'Toyota'},
               {'label': 'Ford', 'value': 'Ford'}
               ],
           value=None,
           placeholder = 'Wybierz producenta'
           ),], className='col'),
          html.Div([dcc.Dropdown(
           id='select-model',
           options=[
               {'label': 'Passat', 'value': 'Passat'},
               {'label': 'Mondeo', 'value': 'Mondeo'},
               {'label': 'Avensis', 'value': 'Avensis'}
               ],
           value=None,
           placeholder = 'Wybierz model'
           ),], className='col'),
          html.Div([
           dcc.Input(
              placeholder='Podaj adres e-mail...',
              type='text',
              value='',
              id='email',
              className='form-control'
              ),
             html.Small('Adres e-mail jest opcjonalny', className='text-muted')
              ], className='col'),
          ], className='row form-group'),
      html.Div([
          html.Div([
              html.Button('Generuj raport', id='gen-report', className='btn btn-lg btn-outline-primary')
              ], className='col text-center')
          ],className='row form-group'),
      dcc.Loading(id='loading-report',
                  children=[html.Div(id='report-div')],
                  type='circle')
    ], className='container')

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


offer_from_layout = html.Div(html.H3('wybrano offer from'))
version_layout = html.Div(html.H3('wybrano version'))
nav = html.Div([
  html.Div([dcc.Link('Overview', href='overview'),], className='col'),
  html.Div([dcc.Link('Offer from', href='offer-from'),], className='col'),
  html.Div([dcc.Link('Version', href='version'),], className='col'),
    ], className='row')

nav1 = html.Div([
    html.Ul([
        html.Li([dcc.Link('Overview', href='overview', className='nav-link', id='nav-overview-btn')], className='nav-item'),
        html.Li([dcc.Link('Offer from', href='offer-from', className='nav-link', id='nav-offer-from-btn')], className='nav-item'),
        html.Li([dcc.Link('Version', href='version', className='nav-link', id='nav-version-btn')], className='nav-item'),
        ], className='nav nav-pills justify-content-center')
    ])

#nav nav-pills nav-fill justify-content-center

@app.callback(
    Output(component_id='select-model', component_property='options'),
    [Input(component_id='select-maker', component_property='value')]
)
def update_models(maker):
    if maker is None:
        raise PreventUpdate
    elif maker == 'VW':
      return [{'label': 'Passat', 'value': 'Passat'}]
    elif maker == 'Toyota':
      return [{'label': 'Avensis', 'value': 'Avensis'}]
    elif maker == 'Ford':
      return [{'label': 'Mondeo', 'value': 'Mondeo'}]
    else: 
        raise PreventUpdate

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
    df = read_data.read_data_from_excel(maker, model)
    df_offer_from = dp.prepare_count(df, 'offer_from')
    df_offer_from2 = df.groupby(['offer_from', 'prod_year'])['price_value_pln_brutto'].mean()
    df_offer_from2 = df_offer_from2.reset_index()
    df_offer_from3 = df.groupby(['offer_from', 'fuel_type'])['N'].count().reset_index()
    df_version = dp.prepare_count(df, 'version')

    datasets = {
         'df': df.to_json(orient='split', date_format='iso'),
         'df_offer_from': df_offer_from.to_json(orient='split', date_format='iso'),
         'df_offer_from2': df_offer_from2.to_json(orient='split', date_format='iso'),
         'df_offer_from3': df_offer_from3.to_json(orient='split', date_format='iso'),
         'df_version': df_version.to_json(orient='split', date_format='iso'),
     }
    
    return json.dumps(datasets)

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
        html.Div(id='report-section1')], 
        )
    return report_page

@app.callback(
    Output(component_id='report-section', component_property='children'),
    [Input(component_id='url', component_property='pathname'),
#     Input(component_id='offer-from-btn', component_property='n_clicks_timestamp'),
     Input(component_id='data-div', component_property='children')]
)
def update_report_section(pathname, jsonified_cleaned_data):
#  return(html.Div([html.H3(version_btn), html.H3(offer_from_btn)]))
  datasets = json.loads(jsonified_cleaned_data)
  #n_offers = pd.read_json(datasets['df']).len()
  if pathname == '/offer-from':
    df_offer_from = pd.read_json(datasets['df_offer_from'], orient='split')
    df_offer_from2 = pd.read_json(datasets['df_offer_from2'], orient='split')
    df_offer_from3 = pd.read_json(datasets['df_offer_from3'], orient='split')
    return offer_from.full_layout(df_offer_from, df_offer_from2, df_offer_from3)
  elif pathname == '/version':
    df_version = pd.read_json(datasets['df_version'], orient='split')
    return version.create_layout(df_version)
  else:
    return html.Div([html.P('Liczba ogłoszeń w próbie: XYZ')])

@app.callback(
    Output(component_id='nav-overview-btn', component_property='className'),
    [Input(component_id='url', component_property='pathname')])
def update_nav_button_overview(pathname):
  if pathname == '/overview':
    return 'nav-link active'
  elif pathname == '/':
    return 'nav-link active'
  else:
    return 'nav-link'

@app.callback(
    Output(component_id='nav-offer-from-btn', component_property='className'),
    [Input(component_id='url', component_property='pathname')])
def update_nav_button_offer_from(pathname):
  if pathname == '/offer-from':
    return 'nav-link active'
  else:
    return 'nav-link'

@app.callback(
    Output(component_id='nav-version-btn', component_property='className'),
    [Input(component_id='url', component_property='pathname')])
def update_nav_button_version(pathname):
  if pathname == '/version':
    return 'nav-link active'
  else:
    return 'nav-link'
      
if __name__ == '__main__':
    app.run_server(debug=True)