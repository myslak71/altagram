import os

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

with open("requirements.txt") as f:
    requirements = [str(req) for req in parse_requirements(f.read())]

with open("requirements-test.txt") as f:
    requirements_test = [str(req) for req in parse_requirements(f.read())]

with open(os.path.join(DIR_PATH, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

extras = {
    "test": requirements_test,
}

setup(
    name="starships",
    packages=find_packages("src"),
    package_dir={"": "src"},
    description="starships",
    long_description=long_description,
    install_requires=requirements,
    python_requires=">=3.9",
    include_package_data=True,
    extras_require=extras,
)
