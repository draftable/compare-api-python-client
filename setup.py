import re
from io import open  # Needed for Python 2.7
from os import path

from setuptools import find_packages, setup

BASE_PATH = path.abspath(path.dirname(__file__))

# Retrieve package version (borrowed from SQLAlchemy)
with open(path.join(BASE_PATH, 'draftable', '__init__.py')) as f:
    VERSION = re.compile(r""".*__version__ = ["'](.*?)['"]""",
                         re.S).match(f.read()).group(1)

setup(
    version=VERSION,
    packages=find_packages(include=['draftable', 'draftable.*']),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    install_requires=['requests', 'six'],
    extras_require={
        'dev': ['flake8', 'isort', 'pylint', 'pytest'],
    },
    scripts=['scripts/dr-compare'],
)
