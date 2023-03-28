import os

from setuptools import setup

from metadata import (NAME, PACKAGE_DIRECTORY, PACKAGES, PYTHON_REQUIRES,
                      SHORT_DESCRIPTION, SOURCE_URL, VERSION)

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + "/release_requirements.txt"

install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name=NAME,
    version=VERSION,
    description=SHORT_DESCRIPTION,
    install_requires=install_requires,
    package_dir=PACKAGE_DIRECTORY,
    packages=PACKAGES,
    python_requires=PYTHON_REQUIRES,
    url=SOURCE_URL,
)