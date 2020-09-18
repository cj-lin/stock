#!/usr/bin/env python
# coding: utf-8


import pathlib

from talib import abstract
import pandas as pd
import pandas_datareader
import yaml


directory = pathlib.Path(__file__).parent.absolute()
config = yaml.safe_load((directory / 'config.yml').read_text())
if config['source'] is None:
    config['source'] = 'yahoo'

data = pandas_datareader.DataReader(
    config['symbol'],
    data_source=config['source'],
    start=config['start'],
    end=config['end']
).rename(columns=lambda x:x.lower())

out = [data]

for func in config['functions']:
    index = getattr(abstract, func)(data)
    if index.ndim == 1:
        index.name = func.lower()
    out.append(index)

pd.concat(out, axis=1).to_csv(f'{directory}/{config["symbol"]}.csv')
