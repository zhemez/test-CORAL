__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2021, National Renewable Energy Laboratory"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.nunemaker@nrel.gov"


import datetime as dt
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
        self._start = self._get_internal_start_date()

        self.initialize_shared_environment()
        self.library = SharedLibrary(self.env, self._alloc, path=library_path)
        self.setup()

    def _get_internal_start_date(self):
        """Return minimum start_date (int or datetime). Used internally."""
        return min([config["project_start"] for config in self.configs])

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

            self.env.process(self._initialize(name, start, config))

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

    def _initialize(self, name, start, config):
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

        idx = self._get_start_idx(start)
        yield self.env.timeout(idx)
        log = {"name": name, "Initialized": self.env.now}

        resources = self._get_shared_resources(config)
        requests = [resource.router.request() for _, resource in resources]

        yield self.env.all_of(requests)
        log["Started"] = self.env.now
        for key, resource in resources:
            config[key] = resource.data

        project = self._run_project(config)
        yield self.env.timeout(project.project_time)
        log["Finished"] = self.env.now

        self._logs.append(
            self._append_request_timing(log, resources, requests)
        )

        for resource, request in zip(resources, requests):
            resource[1].router.release(request)

    def _get_start_idx(self, start) -> int:
        """
        Return index of project start time.

        Parameters
        ----------
        start : float | dt.datetime
            Project start time or datetime stamp.
        """

        if isinstance(start, dt.datetime):
            return int(np.ceil((start - self._start).days * 24))

        return int(np.ceil(start))

    def _get_shared_resources(self, config):
        """
        Return shared resources identified in project config.

        Parameters
        ----------
        config : dict
            Initial ORBIT configuration.
        """

        resources = []
        for k, v in config.items():
            try:
                if "_shared_pool_" in v:
                    target = v.split(":")[1]
                    resources.append((k, self.library.resources[k][target]))

            except TypeError:
                pass

        return resources

    def _run_project(self, config):
        """
        Run configured ORBIT project.

        Parameters
        ----------
        config : dict
            Final ORBIT configuration.
        """

        weather = self._get_current_weather()
        project = ProjectManager(config, weather=weather)
        project.run()

        return project

    def _append_request_timing(self, log, resources, requests):
        """
        Add request timing information to project log.

        Parameters
        ----------
        log : dict
            Project log.
        resources : list
            List of shared resources.
        requests : list
            List of resource requests.
        """

        return {
            **log,
            **{
                f"request-{k}": v.usage_since
                for (k, _), v in zip(resources, requests)
            },
        }

    def _get_current_weather(self):
        """Returns current weather based on `self.env.now`."""

        if self._weather is None:
            return None

        return self._weather[int(np.ceil(self.env.now)) :]
