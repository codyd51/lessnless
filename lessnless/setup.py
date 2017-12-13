from setuptools import setup
from lessnless.version import __version__


setup(
    name='lessnless',
    version=__version__,
    description='Music generator',
    url='https://github.com/codyd51/lessnless',
    author='Phillip Tennen',
    packages=['lessnless'],
    install_requires=[
        'mingus',
    ],
)
