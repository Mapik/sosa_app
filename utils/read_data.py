# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 06:22:28 2019

@author: pim
"""
import pandas as pd
import pathlib

# get relative data folder

def read_data_from_excel(maker, model):
  PATH = pathlib.Path(__file__).parent
  DATA_PATH = PATH.joinpath("../data").resolve()
  if model == "Avensis":
    path = DATA_PATH.joinpath("avensis_only.xlsx")
  elif model == "Passat":
    path = DATA_PATH.joinpath("passat_only.xlsx")
  elif model == "Mondeo":
    path = DATA_PATH.joinpath("mondeo_only.xlsx")
  df = pd.read_excel(path, sheet_name='data')
  df['N'] = 1
  return df