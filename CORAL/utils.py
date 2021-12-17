__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2021, National Renewable Energy Laboratory"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.nunemaker@nrel.gov"


import datetime as dt


def get_installed_capacity_by(df, year) -> int:
    """
    Return installed capacity by specific year.

    Parameters
    ----------
    df : pd.DataFrame
    year : int
    """

    installed_capacity = df.loc[
        df["Date Finished"] < dt.datetime(year, 1, 1, 0, 0)
    ]["capacity"].sum()

    partial = df.loc[
        (df["Date Finished"] > dt.datetime(year, 1, 1, 0, 0))
        & (df["Date Started"] < dt.datetime(year, 1, 1, 0, 0))
    ]

    for _, project in partial.iterrows():
        perc = (dt.datetime(year, 1, 1, 0, 0) - project["Date Started"]) / (
            project["Date Finished"] - project["Date Started"]
        )
        installed_capacity += perc * project["capacity"]

    return installed_capacity
