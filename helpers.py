import datetime as dt
import numpy as np
# Define input files and configurations

input_pipelines = {
'base': "east_coast_analysis/pipelines/pipeline_OWMR2022_base.csv",
'add_ports': "east_coast_analysis/pipelines/pipeline_OWMR2022_add_ports.csv",
'add_ports_fast': "east_coast_analysis/pipelines/pipeline_OWMR2022_add_ports_fast.csv",
'reduce_ports': "east_coast_analysis/pipelines/pipeline_OWMR2022_reduce_ports.csv",
# 'no_akt': "east_coast_analysis/pipelines/pipeline_OWMR2022.csv",
# 'delays': "east_coast_analysis/pipelines/pipeline_OWMR2022_delays.csv",
# 'fast': "east_coast_analysis/pipelines/pipeline_OWMR2022_akt_fast.csv",
}

initial_allocations = {
# Existing
'base2': {
    "wtiv": [('example_wtiv', 2),('example_heavy_lift_vessel', 2)],
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
'base3': {
    "wtiv": [('example_wtiv', 2),('example_heavy_lift_vessel', 3)],
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
    "wtiv": [('example_wtiv', 2), ('example_heavy_lift_vessel', 5)],
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
'add_wtiv_hlv': {
    "wtiv": [('example_wtiv', 2), ('example_heavy_lift_vessel', 3)],
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
    # ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
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
    ['port', 'njwp', [dt.datetime(2028, 1, 1)]],
    ],
'add_wtiv_hlv_ports': [
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    # ['wtiv', 'example_wtiv', [dt.datetime(2026, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    # ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    # # ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2029, 1, 1)]],
    # ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    # ['wtiv', 'example_wtiv', [dt.datetime(2029, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2028, 1, 1)]],
],
'add_4wtiv_hlv_ports': [
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2026, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2027, 1, 1)]],
    # ['wtiv', 'example_heavy_lift_vessel', [dt.datetime(2029, 1, 1)]],
    # ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    # ['wtiv', 'example_wtiv', [dt.datetime(2029, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2028, 1, 1)]],
],
}

current_investment = 150 + 157 + 200 + 400 + 500 #New Bedford, New London, SBMT, NJWP, Charybdis.  Mostly from OWMR
wtiv = 500
port = 400
investments = {  # Include one 'port' in 2022 to cover additioanl grants for ports that are under construction (tradepoint, SBMT, NJWP)
'year': [2022, 2023, 2024, 2025, 2026, 2027, 2028, 2028, 2030, 2031, 2032],
# 'base_wtiv': [wtiv+port, 0, 0, wtiv, 0, 0, 0, 0, 0],
# 'high_wtiv': [wtiv+port, wtiv, 0, wtiv+wtiv, wtiv, 0, 0, 0, 0],
# 'add_port': [port, 0, port, port, port, 0, 0, 0, 0],  #Salem, NJWP2, AKT
# 'add_ports_fast': [port+port+port, 0, port, 0, 0, 0, 0, 0, 0],  #Salem, NJWP2, AKT
# 'add_3hlv_4wtiv_eur_ports': [port+wtiv, ]
'base': [1270, 0, 0, 887, 0, 260, 0, 0, 0, 0, 0],
'add_3hlv_4wtiv_eur_ports': [1270, 0, 0, 887, 500, 1910, 1200, 0, 0, 0, 0]
}  # Fixed bottom ports only 

plot_names_map = {
'baseline': 'Existing \ninfrastructure',
'add_wtiv': 'Add WTIVs',
'add_ports': 'Add ports',
'add_wtiv_ports': 'Add WTIVS \nand ports',
'add_wtiv_eur_ports': 'Add US and Eur WTIVs \n and ports',
'add_hlv_wtiv_eur_ports': 'Add US and Eur WTIVs,  \n US HLVs, and ports',
'reduce_ports': 'Reduced ports',
'add_ports_fast': 'Add ports \n(early constr.)',
'add_wtiv_ports_fast ': 'Add WTIVS \nand ports (early constr.)',
'add_3hlv_4wtiv_eur_ports': 'Expanded \ninfrastructure'
}
