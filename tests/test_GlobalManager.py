__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2021, National Renewable Energy Laboratory"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.nunemaker@nrel.gov"


import os
from copy import deepcopy

from ORBIT import ProjectManager

from CORAL import GlobalManager

DIR = os.path.split(__file__)[0]
LIBRARY_PATH = os.path.join(DIR, "test_library")

BASE = config = {
    "wtiv": "example_wtiv",
    "site": {"depth": 20, "distance": 40},
    "plant": {"num_turbines": 20},
    "turbine": "12MW_generic",
    "project_start": 0,
    "design_phases": [],
    "install_phases": ["TurbineInstallation"],
}


def test_separate_ports():

    # Base case
    project = ProjectManager(BASE)
    project.run()
    base_finished_time = project.installation_time

    # Global resources
    allocations = {"port": [("region_1", 1), ("region_2", 1)]}

    config1 = deepcopy(BASE)
    config1["port"] = "_shared_pool_:region_1"

    config2 = deepcopy(BASE)
    config2["port"] = "_shared_pool_:region_2"

    configs = [config1, config2]

    manager = GlobalManager(configs, allocations, library_path=LIBRARY_PATH)
    manager.run()

    assert manager.logs[0]["Finished"] == base_finished_time
    assert manager.logs[1]["Finished"] == base_finished_time


def test_shared_ports_limited_resources():

    # Base case
    project = ProjectManager(BASE)
    project.run()
    base_finished_time = project.installation_time

    # Global resources
    allocations = {"port": [("region_1", 1)]}

    config1 = deepcopy(BASE)
    config1["port"] = "_shared_pool_:region_1"

    config2 = deepcopy(BASE)
    config2["port"] = "_shared_pool_:region_1"

    configs = [config1, config2]

    manager = GlobalManager(configs, allocations, library_path=LIBRARY_PATH)
    manager.run()

    assert manager.logs[0]["Finished"] == base_finished_time
    assert manager.logs[1]["Finished"] == base_finished_time * 2


def test_shared_ports_sufficient_resources():

    # Base case
    project = ProjectManager(BASE)
    project.run()
    base_finished_time = project.installation_time

    # Global resources
    allocations = {"port": [("region_1", 2)]}

    config1 = deepcopy(BASE)
    config1["port"] = "_shared_pool_:region_1"

    config2 = deepcopy(BASE)
    config2["port"] = "_shared_pool_:region_1"

    configs = [config1, config2]

    manager = GlobalManager(configs, allocations, library_path=LIBRARY_PATH)
    manager.run()

    assert manager.logs[0]["Finished"] == base_finished_time
    assert manager.logs[1]["Finished"] == base_finished_time
