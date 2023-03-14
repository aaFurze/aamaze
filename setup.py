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
    version="0.0.3",
    description="A python library for generating, solving and displaying mazes.",
    install_requires=install_requires,
    package_dir={"": "aamaze"},
    packages=["", "generation", "graphics", "solving"],
    python_requires='>=3.7',
    url="https://github.com/aaFurze/aamaze",

)