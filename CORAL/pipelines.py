__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2021, National Renewable Energy Laboratory"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.nunemaker@nrel.gov"


from copy import deepcopy

import pandas as pd
from ORBIT import load_config


class Pipeline:
    """Base class for modeling offshore wind project pipelines."""

    def __init__(self, projects_fp, base_config):
        """
        Creates an instance of `Pipeline`.

        Parameters
        ----------
        projects_fp : str
            Filepath
        base_config : str
            Filepath
        """

        self.projects = pd.read_csv(projects_fp, parse_dates=["start_date"])
        self.base = load_config(base_config)
        self.configs = self.build_configs()

    def build_configs(self):
        """Iterate through projects in `self.projects` and build ORBIT configs."""

        configs = []
        for _, data in self.projects.iterrows():

            config = deepcopy(self.base)
            config["project_name"] = data["name"]
            config["project_coords"] = (data["lat"], data["lon"])
            config["project_start"] = data["start_date"]

            config["turbine"] = data["turbine"]
            config["plant"]["num_turbines"] = data["num_turbines"]

            config["site"]["depth"] = data["depth"]
            config["site"]["distance_to_landfall"] = data["distance_to_shore"]

            config["port"] = ":".join(["_shared_pool_", data["port_region"]])

            config = self.add_substructure_specific_config(
                config, data["substructure"]
            )
            configs.append(config)

        return configs

    def add_substructure_specific_config(self, config, substructure):
        """
        Append substructure specific configurations.

        Parameters
        ----------
        config : dict
            ORBIT config
        substructure : str
            Substructure type
        """

        if substructure == "monopile":

            # Design Phases
            config["design_phases"] += [
                "MonopileDesign",
                "ScourProtectionDesign",
            ]

            # Install Phases
            config["install_phases"]["ScourProtectionInstallation"] = 0
            config["install_phases"]["MonopileInstallation"] = 0
            config["install_phases"]["TurbineInstallation"] = 0
            # config["install_phases"]["MonopileInstallation"] = ("ScourProtectionInstallation", 0.5)
            # config["install_phases"]["TurbineInstallation"] = ("MonopileInstallation", 0.2)

        else:
            raise TypeError(f"Substructure '{substructure}' not supported.")

        return config
