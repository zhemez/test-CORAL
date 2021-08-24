__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2021, National Renewable Energy Laboratory"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.nunemaker@nrel.gov"


from copy import deepcopy
from collections import Counter

import numpy as np
from ORBIT import ProjectManager
from simpy import Environment

from .library import SharedLibrary


class GlobalManager:
    """Class to manage concurrent ORBIT simulations with shared resources."""

    def __init__(self, configs, allocations, weather=None, library_path=None):
        """
        Creates an instance of `GlobalManager`.

        Parameters
        ----------
        configs : list
            List of ORBIT configurations to run.
        library_path : str
            Path to shared library items.
        allocations : dict
            Number of each library item that exists in the shared environment.
        """

        self._logs = []
        self._counter = Counter()
        self._weather = weather
        self._alloc = allocations
        self.configs = [deepcopy(config) for config in configs]

        self.initialize_shared_environment()
        self.library = SharedLibrary(self.env, self._alloc, path=library_path)

    @property
    def logs(self):
        """Return post-processed logs."""

        processed = []
        for log in self._logs:

            new = deepcopy(log)
            for key, value in log.items():
                if key.startswith("request-"):
                    new[f"delay-{key.replace('request-', '')}"] = (
                        value - new["Initialized"]
                    )

            processed.append(new)

        return processed

    def initialize_shared_environment(self):
        """Initializes `simpy.Environment` for managing shared resources."""

        self.env = Environment()

    def setup(self):
        """Initialize the projects."""

        for config in self.configs:

            name = self._get_unique_name(config.pop("project_name", "Project"))
            start = config.pop("project_start", 0)

            self.env.process(self._run_project(name, start, config))

    def _get_unique_name(self, name):
        """
        Returns a unique name based on instances in `self._counter`.

        Parameters
        ----------
        name : str
            Base name.
        """

        self._counter[name] += 1
        if self._counter[name] == 1 and name != "Project":
            return name

        return f"{name} {self._counter[name]}"

    def run(self):
        """Main simulation run method."""

        self.env.run()

    def _run_project(self, name, start, config):
        """
        Run an individual project configuration.

        Parameters
        ----------
        name : str
            Project handle.
        start : int | float
            Time to initialize project.
        config : dict
            ORBIT configuration.
        """

        log = {"name": name}
        yield self.env.timeout(start)
        log["Initialized"] = self.env.now

        keys = [k for k in list(config) if k in list(self.library.resources)]
        resources = [
            self.library.resources[k]
            for k in keys
            if config[k] == "_shared_pool_"
        ]
        requests = [resource.router.request() for resource in resources]

        yield self.env.all_of(requests)
        log["Started"] = self.env.now

        for key, resource in zip(keys, resources):
            config[key] = resource.data

        weather = self._get_current_weather()
        project = ProjectManager(config, weather=weather)
        project.run()

        yield self.env.timeout(project.project_time)
        log["Finished"] = self.env.now
        self._logs.append(
            {
                **log,
                **{
                    f"request-{k}": v.usage_since
                    for k, v in zip(keys, requests)
                },
            }
        )

        for resource, request in zip(resources, requests):
            resource.router.release(request)

    def _get_current_weather(self):
        """Returns current weather based on `self.env.now`."""

        if self._weather is None:
            return None

        return self._weather[int(np.ceil(self.env.now)) :]
