import os
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as mpl
from copy import deepcopy

mpl.rcParams['hatch.linewidth'] = 0.2  # previous pdf hatch linewidth

from ORBIT.core.library import initialize_library
from CORAL import SharedLibrary, GlobalManager, Pipeline
from CORAL.utils import get_installed_capacity_by

# name scenarios
scenario_names = [
    '_unlimited_akt',
    '_unlimited_no_akt',
    '_limitWTIV',
    '_limitWTIV',
    '_delayedPort',
    # 1 year construction delays on SBMT, AKT, Salem, New London
    '_delayedPort_limitWTIV',
    '_limitFeeder'
]

pipeline_list = [
    "east_coast_analysis/pipeline_OWMR2022_akt.csv",
    "east_coast_analysis/pipeline_OWMR2022.csv",
    "east_coast_analysis/pipeline_OWMR2022_akt.csv",
    "east_coast_analysis/pipeline_OWMR2022_akt.csv",
    "east_coast_analysis/pipeline_OWMR2022_delays.csv",
    "east_coast_analysis/pipeline_OWMR2022_delays.csv",
    "east_coast_analysis/pipeline_OWMR2022_akt.csv",
]
#### Define initial port and vessel configuration  (all the same for now)
allocations_list = [
    {"wtiv": ('example_wtiv', 1),
    "feeder": ('example_feeder', 10),
    "port": [
        ('new_bedford', 1),
        ('new_london', 1),
        ('njwp', 1),
        ('sbmt', 1),
        ('portsmouth', 1),
        ('salem', 1),
        ('tradepoint', 1),
        ('akt', 1)
    ],
},
] * len(pipeline_list) + [
    {"wtiv": ('example_wtiv', 1),
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
    ],
},
]

future_resources_list = [
[
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2026, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2029, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2025, 1, 1)]],
],  # _unlimited_akt
[
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2026, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2029, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2025, 1, 1)]],
],  # _unlimited_no_akt
[
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2025, 1, 1)]],
],  # _limitWTIV
[
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2025, 1, 1)]],
],  # _limitWTIV
[
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2026, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2029, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2025, 1, 1)]],
],  # _delayedPort
[
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2025, 1, 1)]],
],  # _delayedPort_limitWTIV
[
    ['wtiv', 'example_wtiv', [dt.datetime(2025, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2026, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2028, 1, 1)]],
    ['wtiv', 'example_wtiv', [dt.datetime(2029, 1, 1)]],
    ['port', 'njwp', [dt.datetime(2025, 1, 1)]],
    ['feeder', 'example_feeder', [dt.datetime(2024, 1, 1)]],
    ['feeder', 'example_feeder', [dt.datetime(2025, 1, 1)]],
    ['feeder', 'example_feeder', [dt.datetime(2026, 1, 1)]],
    ['feeder', 'example_feeder', [dt.datetime(2027, 1, 1)]],
    ['feeder', 'example_feeder', [dt.datetime(2028, 1, 1)]],
    ['feeder', 'example_feeder', [dt.datetime(2029, 1, 1)]],
    ['feeder', 'example_feeder', [dt.datetime(2030, 1, 1)],]
],  # _limitFeeder
]

if __name__ == '__main__':
    initialize_library(os.path.join(os.getcwd(), "east_coast_analysis/library"))

    weather = pd.read_csv("east_coast_analysis/library/weather/vineyard_wind_repr_with_whales.csv", parse_dates=["datetime"]).set_index("datetime")

    library_path = os.path.join(os.getcwd(), "east_coast_analysis/library")

    for allocations, future_resources, pipeline, name in zip(allocations_list, future_resources_list, pipeline_list, scenario_names):

        projects = os.path.join(os.getcwd(), pipeline)
        base = os.path.join(os.getcwd(), "east_coast_analysis/base.yaml")
        pipeline = Pipeline(projects, base, regional_ports=False)

        num_wtiv = len(allocations['wtiv'])
        num_port = len(allocations['port'])

        manager = GlobalManager(pipeline.configs, allocations, library_path=library_path, weather=weather)

        new_wtiv = [1 for fr in future_resources if 'wtiv' in fr]
        new_ports = [1 for fr in future_resources if 'port' in fr]

        total_wtiv = np.sum([num_wtiv]+new_wtiv)
        total_ports = np.sum([num_port]+new_ports)

        fig_name = str(total_wtiv)+'wtiv_'+str(total_ports)+'ports_'+name


        for f in future_resources:
            manager.add_future_resources(f[0], f[1], f[2])

        # Run simulation with future resources
        manager.run()
        print('Simulation complete')

        # Postprocessing
        df = pd.DataFrame(manager.logs).iloc[::-1]
        df = df.reset_index(drop=True).reset_index()

        # Save csv
        csv_name = fig_name + '_data.csv'
        df.to_csv(csv_name)

        # Assign ports to projects
        port_map = pipeline.projects[["name", "associated_port", "capacity"]].set_index("name").to_dict()['associated_port']
        df['port'] = [port_map[name] for name in df['name']]

        capacity_map = pipeline.projects[["name", "capacity"]].set_index("name").to_dict()['capacity']
        df['capacity'] = [capacity_map[name] for name in df['name']]

        # Plot results
        fig = plt.figure(figsize=(10, 6), dpi=300)
        ax = fig.add_subplot(111)

        df["Date Finished"].plot(kind="barh", ax=ax, zorder=4, label="Project Installation", color="#b1b1b1")
        df["Date Started"].plot(kind="barh", color="#e9e9e9", ax=ax, zorder=4, label="Project Delay", hatch="////", linewidth=0.5)
        df["Date Initialized"].plot(kind='barh', ax=ax, zorder=4, label="__nolabel__", color='w')

        # Plot formatting
        ax.set_xlabel("")
        ax.set_ylabel("")
        _ = ax.set_yticklabels(df['name'])
        plt.yticks(fontsize=6)
        ax.legend()
        ax.set_xlim(manager._start - dt.timedelta(days=30), dt.date(2036, 6, 1) + dt.timedelta(days=30))#df["Date Finished"].max() + dt.timedelta(days=30))

        ax.axvline(dt.date(2031, 1, 1), lw=0.5, ls="--", color="k", zorder=6)
        installed_capacity = get_installed_capacity_by(df, 2031)
        ax.text(x=dt.date(2031, 4, 1), y=20, s=f"Capacity installed \nby end of 2030: \n{installed_capacity/1000:,.3} GW", fontsize=20)

        fig.subplots_adjust(left=0.25)

        fname_d = 'east_coast_analysis/figures/sc_roadmap_gaps/deployment_'+fig_name+'.png'
        fig.savefig(fname_d, dpi=300)

        ### Annual throughput

        res = []

        for _, project in df.iterrows():

            if project["Date Finished"].year == project["Date Started"].year:
                res.append((project["Date Finished"].year, project["port"], project["capacity"]))

            else:

                perc = (project["Date Finished"].date() - dt.date(project["Date Finished"].year, 1, 1)) /\
                    (project["Date Finished"] - project["Date Started"])

                res.append((project["Date Finished"].year, project["port"], perc * project["capacity"]))
                res.append((project["Date Started"].year, project["port"], (1 - perc) * project["capacity"]))

        throughput = pd.DataFrame(res, columns=["year", "port", "capacity"]).pivot_table(
            index=["year"],
            columns=["port"],
            aggfunc="sum",
            fill_value=0.
        )["capacity"]

        fig = plt.figure(figsize=(6, 4), dpi=200)
        ax = fig.add_subplot(111)

        throughput.plot(ax=ax, lw=0.7)

        ax.set_ylim(0, 2000)

        ax.set_ylabel("Annual Capacity Throughput (MW)")
        ax.set_xlabel("")

        plt.xticks(rotation=0, fontsize=6)
        plt.yticks(fontsize=6)

        ax.legend(fontsize=6, ncol=5)
        fname_t = 'east_coast_analysis/figures/sc_roadmap_gaps/throughput_'+fig_name+'.png'
        fig.savefig(fname_t, dpi=300)

        # plt.show()
