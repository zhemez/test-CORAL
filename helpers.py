import datetime as dt
import numpy as np
# Define input files and configurations

input_pipelines = {
'base': "east_coast_analysis/pipelines/pipeline_OWMR2022_base.csv",
'add_ports': "east_coast_analysis/pipelines/pipeline_OWMR2022_add_ports.csv",
}

initial_allocations = {
'base': {
    "wtiv": [('example_wtiv', 2),('example_heavy_lift_vessel', 2)],
    "feeder": ('example_feeder', 2),
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
'us_wtiv': {
    "wtiv": [('example_wtiv', 2),('example_heavy_lift_vessel', 3)],  # Need an extra HLV from the start of th esimulation
    "feeder": ('example_feeder', 2),
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
 'us_feeder': {
    "wtiv": [('example_wtiv', 4),('example_heavy_lift_vessel', 4)],
    "feeder": ('example_feeder', 2),
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
    ],
'us_wtiv': [
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2026, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2028, 1, 1)]],
],
'us_feeder': [
    # ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    # ['wtiv', 'example_wtiv', [dt.datetime(2026, 1, 1)]],
    # ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    # ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    # ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    # ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    # ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    ['feeder', 'example_feeder', [dt.datetime(2026,1,1)]],
    ['feeder', 'example_feeder', [dt.datetime(2026,1,1)]],
    # ['feeder', 'example_feeder', [dt.datetime(2025,1,1)]],
    # ['feeder', 'example_feeder', [dt.datetime(2025,1,1)]],
    # ['feeder', 'example_feeder', [dt.datetime(2025,1,1)]],
    # ['feeder', 'example_feeder', [dt.datetime(2025,1,1)]],
    ['port', 'njwp', [dt.datetime(2028, 1, 1)]],
],
}

current_investment = 150 + 157 + 200 + 400 + 500 #New Bedford, New London, SBMT, NJWP, Charybdis.  Mostly from OWMR
wtiv = 500
port = 400
investments = {
    'year': [2022, 2023, 2024, 2025, 2026, 2027, 2028, 2028, 2030, 2031, 2032],
    'base': [1270, 0, 0, 887, 0, 260, 0, 0, 0, 0, 0],
    'us_wtiv': [1270, 0, 0, 887, 500, 1910, 1200, 0, 0, 0, 0]
}  # Fixed bottom ports only

plot_names_map = {
'baseline': 'Baseline',
'US_WTIV': 'US_WTIV',
'US_feeder': 'US_feeder'
}
