from setuptools import setup, find_packages
from io import open as io_open


readme = None
with io_open("README.rst") as fd:
  readme = fd.read()
setup(name='draftable_compare_api',
      version='1.0.9',
      description='Draftable Compare API - Python Client Library',
      long_description=readme,
      keywords='compare documents draftable api pdf word powerpoint',
      url='https://github.com/draftable/compare-api-python-client',
      author='Draftable',
      author_email='hello@draftable.com',
      license='MIT',
      packages=find_packages(include=('draftable*',)),
      entry_points={'console_scripts': ['draftable=draftable.cli:main'], },
      install_requires=['requests', 'argopt'],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
      ])
