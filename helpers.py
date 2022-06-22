import datetime as dt

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
    ['port', 'njwp', [dt.datetime(2028, 1, 1)]],
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
