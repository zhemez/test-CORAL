import datetime as dt
import numpy as np
# Define input files and configurations

input_pipelines = {
'base': "east_coast_analysis/pipelines/pipeline_OWMR2022_base.csv",
'add_ports': "east_coast_analysis/pipelines/pipeline_OWMR2022_add_ports.csv",
'add_ports_fast': "east_coast_analysis/pipelines/pipeline_OWMR2022_add_ports_fast.csv",
# 'no_akt': "east_coast_analysis/pipelines/pipeline_OWMR2022.csv",
# 'delays': "east_coast_analysis/pipelines/pipeline_OWMR2022_delays.csv",
# 'fast': "east_coast_analysis/pipelines/pipeline_OWMR2022_akt_fast.csv",
}

initial_allocations = {
# Existing
'base': {
    "wtiv": ('example_wtiv', 1),
    "feeder": ('example_feeder', 4),
    "port": [
        ('new_bedford', 1),
        ('new_london', 1),
        ('njwp', 1),
        ('sbmt', 1),
        ('portsmouth', 1),
        ('salem', 1),
        ('tradepoint', 1),
        ('akt', 1)
    ]
    },
'add_wtiv': {
    "wtiv": ('example_wtiv', 2),
    "feeder": ('example_feeder', 4),
    "port": [
        ('new_bedford', 1),
        ('new_london', 1),
        ('njwp', 1),
        ('sbmt', 1),
        ('portsmouth', 1),
        ('salem', 1),
        ('tradepoint', 1),
        ('akt', 1)
    ]
    },
}

future_allocations = {
'base': [
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    # ['port', 'njwp', [dt.datetime(2028, 1, 1)]],
    ],
'high_wtiv':[
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2026, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2029, 1, 1)]],
    ],
'add_ports':[
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2028, 1, 1)]],
    ],
'add_wtiv_ports':[
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2026, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2029, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2028, 1, 1)]],
    ],
}

current_investment = 150 + 157 + 200 + 400 + 500 #New Bedford, New London, SBMT, NJWP, Charybdis
wtiv = 500
port = 400
investments = {
'year': [2022, 2023, 2024, 2025, 2026, 2027, 2028, 2028, 2030],
'base_wtiv': [wtiv, 0, 0, wtiv, 0, 0, 0, 0, 0],
'high_wtiv': [wtiv, wtiv, 0, wtiv+wtiv, wtiv, 0, 0, 0, 0],
'add_port': [0, 0, port, port, port, 0, 0, 0, 0],  #Salem, NJWP2, AKT
'add_ports_fast': [port+port, 0, port, 0, 0, 0, 0, 0, 0],  #Salem, NJWP2, AKT
}
