__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2021, National Renewable Energy Laboratory"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.nunemaker@nrel.gov"


from copy import deepcopy

from ORBIT import ProjectManager
from simpy import Environment

from .library import SharedLibrary


class GlobalManager:
    """Class to manage concurrent ORBIT simulations with shared resources."""

    def __init__(self, configs, library_path, allocations):
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

        self.configs = [deepcopy(config) for config in configs]
        self._path = library_path
        self._alloc = allocations

        self.initialize_shared_environment()
        self.library = SharedLibrary(self.env, self._path, self._alloc)
        self.projects = []

    def initialize_shared_environment(self):
        """Initializes `simpy.Environment` for managing shared resources."""

        self.env = Environment()

    def setup(self):
        """Initialize the projects."""

        for i, config in enumerate(self.configs):
            self.env.process(self._run_project(i, config))

    def run(self):
        """Main simulation run method."""

        self.env.run()

    def _run_project(self, i, config):
        """
        Run an individual project configuration.

        Parameters
        ----------
        i : int
            Project number. TODO: Make this more flexible.
        config : dict
            ORBIT configuration.
        """

        keys = [k for k in list(config) if k in list(self.library.resources)]
        resources = [self.library.resources[k] for k in keys]
        requests = [resource.router.request() for resource in resources]

        yield self.env.all_of(requests)
        print(f"Project {i} starting at {self.env.now}.")

        for key, resource in zip(keys, resources):
            config[key] = resource.data

        project = ProjectManager(config)
        project.run()
        self.projects.append(project)

        yield self.env.timeout(project.project_time)
        print(f"Project {i} done at {self.env.now}.")

        for resource, request in zip(resources, requests):
            resource.router.release(request)
