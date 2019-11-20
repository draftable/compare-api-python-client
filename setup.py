import os
import re

from setuptools import find_packages, setup

base_path = os.path.dirname(__file__)

# Get the version (borrowed from SQLAlchemy)
with open(os.path.join(base_path, 'draftable', '__init__.py')) as fp:
    version = re.compile(r".*__version__ = '(.*?)'",
                         re.S).match(fp.read()).group(1)

setup(name='draftable_compare_api',
      version=version,
      description='Draftable Compare API - Python Client Library',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',  # This is important. Ignore warning from distutils.
      keywords='compare documents draftable api pdf word powerpoint',
      url='https://github.com/draftable/compare-api-python-client',
      author='Draftable',
      author_email='hello@draftable.com',
      license='MIT',
      packages=find_packages(include=['draftable*'], exclude=['test*py']),
      install_requires=['requests', 'six'],
      scripts=['scripts/dr-compare'],
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
