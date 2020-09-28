#!/usr/bin/env python
# coding: utf-8


import pathlib

from talib.abstract import *
import pandas
import pandas_datareader
import yaml


directory = pathlib.Path(__file__).parent.absolute()
config = yaml.safe_load((directory / 'config.yml').read_text())
if config['source'] is None:
    config['source'] = 'yahoo'

org_data = pandas_datareader.DataReader(
    config['symbol'],
    data_source=config['source'],
    start=config['start'],
    end=config['end']
).rename(columns=lambda x:x.lower())

data = [org_data]

for functions in config['functions']:
    index = Function(functions['funcname'].lower())(org_data, **functions['params'])
    if index.ndim == 1:
        index.name = functions['funcname'].lower() + functions['suffix']
    else:
        index.rename(columns=lambda x:x + functions['suffix'], inplace=True)
    data.append(index)

pandas.concat(data, axis=1).to_csv(f'{directory}/{config["symbol"]}.csv')
