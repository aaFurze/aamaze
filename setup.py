import os

from setuptools import setup

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name="aamaze",
    version="0.0.1",
    description="A python library for generating, solving and displaying mazes.",
    install_requires=install_requires,
    package_dir={"": "aamaze"},
    packages=["", "generation", "graphics", "solving"],
    url="https://github.com/aaFurze/aamaze",

)