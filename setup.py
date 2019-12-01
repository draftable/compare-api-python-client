import re
from io import open  # Needed for Python 2.7
from os import path

from setuptools import find_packages, setup

BASE_PATH = path.abspath(path.dirname(__file__))

# Retrieve package version (borrowed from SQLAlchemy)
with open(path.join(BASE_PATH, 'draftable', '__init__.py')) as f:
    VERSION = re.compile(r""".*__version__ = ["'](.*?)['"]""",
                         re.S).match(f.read()).group(1)

# Use our README.md for the long description
with open(path.join(BASE_PATH, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='draftable_compare_api',
    version=VERSION,
    description='Client library for the Draftable document comparison API',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/draftable/compare-api-python-client',
    author='Draftable',
    author_email='contact@draftable.com',
    license='MIT',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        'Topic :: Software Development :: Libraries',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords='draftable api compare comparison comparisons \
              pdf word document documents doc docx powerpoint presentation presentations ppt pptx',
    project_urls={
        'Documentation': 'https://github.com/draftable/compare-api-python-client/README.md',
        'Source': 'https://github.com/draftable/compare-api-python-client',
        'Tracker': 'https://github.com/draftable/compare-api-node-client/issues'
    },
    packages=find_packages(include=['draftable', 'draftable.*']),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    install_requires=['requests', 'six'],
    extras_require={
        'dev': ['flake8', 'isort', 'pylint', 'pytest'],
    },
    scripts=['scripts/dr-compare'],
)
