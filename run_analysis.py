import os
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch
from copy import deepcopy

mpl.rcParams['hatch.linewidth'] = 0.2  # previous pdf hatch linewidth

from ORBIT.core.library import initialize_library
from CORAL import SharedLibrary, GlobalManager, Pipeline
from CORAL.utils import get_installed_capacity_by

from helpers import input_pipelines as ip
from helpers import initial_allocations as ia
from helpers import future_allocations as fa
from helpers import investments as inv
from helpers import plot_names_map as pnm

scenarios = {
    'baseline': {'pipeline': ip['base'],
                 'initial': ia['base2'],
                 'future': fa['base'],
                 'invest': [inv['base_wtiv']]},
    # 'add_wtiv': {'pipeline': ip['base'],
    #              'initial': ia['base'],
    #              'future': fa['high_wtiv'],
    #              'invest': [inv['high_wtiv']],},
    # 'add_ports': {'pipeline': ip['add_ports'],
    #              'initial': ia['base'],
    #              'future': fa['add_ports'],
    #              'invest': [inv['base_wtiv'], inv['add_port']],},
     # 'reduce_ports': {'pipeline': ip['reduce_ports'],
     #              'initial': ia['base'],
     #              'future': fa['high_wtiv'],
     #              'invest': [inv['high_wtiv']],},
     # 'add_ports_fast': {'pipeline': ip['add_ports_fast'],
     #              'initial': ia['base'],
     #              'future': fa['add_ports'],
     #              'invest': [inv['base_wtiv'], inv['add_ports_fast']],},
     # 'add_wtiv_ports': {'pipeline': ip['add_ports'],
     #           'initial': ia['base'],
     #           'future': fa['add_wtiv_ports'],
     #           'invest': [inv['high_wtiv'], inv['add_port']],},
     # 'add_wtiv_ports_fast': {'pipeline': ip['add_ports_fast'],
     #              'initial': ia['base'],
     #              'future': fa['add_wtiv_ports'],
     #              'invest': [inv['high_wtiv'], inv['add_ports_fast']],},
     # 'add_wtiv_eur_ports': {'pipeline': ip['add_ports'],
     #              'initial': ia['add_wtiv'],
     #              'future': fa['add_wtiv_ports'],
     #              'invest': [inv['high_wtiv'], inv['add_port']],},
     # 'add_2hlv_wtiv_eur_ports': {'pipeline': ip['add_ports'],
     #              'initial': ia['base2'],
     #              'future': fa['add_4wtiv_hlv_ports'],
     #              'invest': [inv['high_wtiv'], inv['add_port']],},
     #  'add_3hlv_wtiv_eur_ports': {'pipeline': ip['add_ports'],
     #               'initial': ia['base3'],
     #               'future': fa['add_wtiv_hlv_ports'],
     #               'invest': [inv['high_wtiv'], inv['add_port']],},
     'add_3hlv_4wtiv_eur_ports': {'pipeline': ip['add_ports'],
                  'initial': ia['base3'],
                  'future': fa['add_4wtiv_hlv_ports'],
                  'invest': [inv['high_wtiv'], inv['add_port']],},
}
invest_year_base = [dt.datetime(yi, 1, 1) for yi in inv['year']]
cumsum_plot = True

if __name__ == '__main__':
    # Intialize scripts

    initialize_library(os.path.join(os.getcwd(), "east_coast_analysis/library"))

    weather = pd.read_csv("east_coast_analysis/library/weather/vineyard_wind_repr_with_whales.csv", parse_dates=["datetime"]).set_index("datetime")

    library_path = os.path.join(os.getcwd(), "east_coast_analysis/library")

    names = []
    capacity_2030 = []
    investment_2030 = []

    for name, scenario in scenarios.items():
        # Extract scenario parameters
        pipeline = scenario['pipeline']
        allocations = scenario['initial']
        future_resources = scenario['future']
        investment = scenario['invest']

        projects = os.path.join(os.getcwd(), pipeline)
        base = os.path.join(os.getcwd(), "east_coast_analysis/base.yaml")
        pipeline = Pipeline(projects, base, regional_ports=False)

        num_wtiv = allocations['wtiv'][1]
        num_port = len(allocations['port'])

        manager = GlobalManager(pipeline.configs, allocations, library_path=library_path, weather=weather)

        new_wtiv = [1 for fr in future_resources if 'wtiv' in fr]
        new_ports = [1 for fr in future_resources if 'port' in fr]

        # total_wtiv = np.sum([num_wtiv]+new_wtiv)
        total_wtiv = 99
        total_ports = np.sum([num_port]+new_ports)

        # fig_name = str(total_wtiv)+'wtiv_'+str(total_ports)+'ports_'+name
        fig_name = name


        for f in future_resources:
            manager.add_future_resources(f[0], f[1], f[2])

        # Run simulation with future resources
        manager.run()
        print('Simulation complete')

        # Postprocessing
        df = pd.DataFrame(manager.logs).iloc[::-1]
        df = df.reset_index(drop=True).reset_index()

        # Save csv
        csv_name = 'east_coast_analysis/figures/sc_roadmap_gaps/' + fig_name + '_data.csv'
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
        ax.text(x=dt.date(2031, 4, 1), y=24, s=f"Capacity installed \nby end of 2030: \n{installed_capacity/1000:,.3} GW", fontsize=20)

        # Add cumulative investments
        if cumsum_plot == True:
            invest_year = deepcopy(invest_year_base)
            annual_invest = [0] * len(invest_year_base)
            for i in investment:
                annual_invest = [x+y for x,y in zip(annual_invest, i)]
            if df['Date Finished'].max() > invest_year_base[-1]:
                invest_year.append(df['Date Finished'].max())
                annual_invest.append(annual_invest[-1])
            # else:
            #     invest_year = invest_year_base

            axR = ax.twinx()
            axR.plot(invest_year, np.cumsum(annual_invest), 'r', zorder=7)
            axR.set_ylabel('Additional investment required, $M')
            axR.set_ylim([0,8000])
            axR.get_yaxis().set_major_formatter(
                mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
            axR.tick_params(axis='y', colors='red')
            axR.yaxis.label.set_color('red')

        fig.subplots_adjust(left=0.25)

        fname_d = 'east_coast_analysis/figures/sc_roadmap_gaps/deployment_'+fig_name+'.png'
        fig.savefig(fname_d, dpi=300)

        ### Annual throughput

        res = []

        for _, project in df.iterrows():

            if project["Date Finished"].year == project["Date Started"].year:
                res.append((project["Date Finished"].year, project["port"], project["capacity"]))

            else:

                total = project["Date Finished"].date() - project["Date Started"].date()
                for year in np.arange(project["Date Started"].year, project["Date Finished"].year + 1):
                    if year == project["Date Started"].year:
                        perc = (dt.date(year + 1, 1, 1) - project["Date Started"].date()) / total

                    elif year == project["Date Finished"].year:
                        perc = (project["Date Finished"].date() - dt.date(year, 1, 1)) / total

                    else:
                        perc = (dt.date(year + 1, 1, 1) - dt.date(year, 1, 1)) / total

                    res.append((year, project["port"], perc * project["capacity"]))

        throughput = pd.DataFrame(res, columns=["year", "port", "capacity"]).pivot_table(
            index=["year"],
            columns=["port"],
            aggfunc="sum",
            fill_value=0.
        )["capacity"]

        fig = plt.figure(figsize=(6, 4), dpi=200)
        ax = fig.add_subplot(111)

        throughput.plot.bar(ax=ax, width=0.75)

        ax.set_ylim(0, 2000)

        ax.set_ylabel("Annual Capacity Throughput (MW)")
        ax.set_xlabel("")

        plt.xticks(rotation=0, fontsize=6)
        plt.yticks(fontsize=6)

        ax.legend(fontsize=6, ncol=5)
        fname_t = 'east_coast_analysis/figures/sc_roadmap_gaps/throughput_'+fig_name+'.png'
        fig.savefig(fname_t, dpi=300)

        # plt.show()
        # Save summary statistics
        names.append(name)
        capacity_2030.append(installed_capacity/1000)
        investment_2030.append(np.cumsum([annual_invest])[-1])

    # Plot
    fig = plt.figure(figsize=(6, 4), dpi=200)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    width = 0.4

    x_ind = np.arange(len(names))
    ax1.bar(x_ind-width/2, capacity_2030, width, color='#3C2AC0')
    ax1.set_ylabel('Installed capacity by end of 2030, GW')
    ax1.set_ylim([0,35])

    ax2.bar(x_ind+width/2, investment_2030, width, color='#FFA319')
    ax2.set_ylabel('Additional investment required, $M')
    ax2.set_ylim([0,5000])
    ax2.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    ax1.set_xticks(x_ind)
    plot_names = [pnm[n] for n in names]
    ax1.set_xticklabels(plot_names, rotation=45)

    handles = [
        Patch(facecolor=color, label=label)
        for label, color in zip(['Installed capacity', 'Investment'], ['#3C2AC0', '#FFA319'])
    ]

    ax1.legend(handles=handles, loc='upper left');

    fname_sum = 'east_coast_analysis/figures/sc_roadmap_gaps/scenario_summary.png'
    fig.savefig(fname_sum, bbox_inches='tight', dpi=300)
