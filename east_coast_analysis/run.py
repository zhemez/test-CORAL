__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2021, National Renewable Energy Laboratory"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.nunemaker@nrel.gov"


import os

import pandas as pd

from CORAL import Pipeline, GlobalManager, pipelines

DIR = os.path.split(__file__)[0]


def run():
    # Pipeline information
    projects = os.path.join(DIR, "example_pipeline.csv")
    base = os.path.join(DIR, "base.yaml")
    pipeline = Pipeline(projects, base)

    # CORAL Configuration
    library_path = os.path.join(DIR, "library")
    allocations = {
        "wtiv": ("example_wtiv", 3),
        "feeder": ("example_feeder", 6),
        "port": [("northeast", 2), ("central", 1), ("south", 1)],
    }

    # Setup and run
    manager = GlobalManager(
        pipeline.configs, allocations, library_path=library_path
    )
    manager.setup()
    manager.run()

    # Outputs
    logs = pd.DataFrame(manager.logs)
    logs.to_csv(os.path.join(DIR, "outputs", "project_logs.csv"))


if __name__ == "__main__":

    run()
