# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 06:22:28 2019

@author: pim
"""
import pandas as pd
import pathlib
import datetime as dt

# get relative data folder

def read_data_from_excel(maker=None, model=None):
  print('{} - START read_data_from_excel'.format(dt.datetime.now()))
  PATH = pathlib.Path(__file__).parent
  DATA_PATH = PATH.joinpath("../data").resolve()
  if model == "Avensis":
    path = DATA_PATH.joinpath("avensis_only.xlsx")
  elif model == "Passat":
    path = DATA_PATH.joinpath("passat_only.xlsx")
  elif model == "Mondeo":
    path = DATA_PATH.joinpath("mondeo_only.xlsx")
  else:
    path = DATA_PATH.joinpath('all_models.xlsx')
  df = pd.read_excel(path, sheet_name='data')
  df['N'] = 1
  print('{} - END read_data_from_excel'.format(dt.datetime.now()))
  return df

def read_data_from_csv(maker=None, model=None):
  print('{} - START read_data_from_excel'.format(dt.datetime.now()))
  PATH = pathlib.Path(__file__).parent
  DATA_PATH = PATH.joinpath("../data").resolve()
  path = DATA_PATH.joinpath('all_models.csv')
  df = pd.read_csv(path, sep=';')
  df['N'] = 1
  print('{} - END read_data_from_excel'.format(dt.datetime.now()))
  return df