"""Distribution setup."""

from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(
    name="CORAL",
    description=long_description,
    packages=find_packages(),
    install_requires=["orbit-nrel==1.0.6", "jupyterlab"],
)
