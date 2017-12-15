from setuptools import setup

setup(
    name='meteogram',
    version='',
    packages=['meteogram'],
    url='',
    license='',
    author='Martin Høy',
    author_email='martin.hoy@pvv.ntnu.no',
    description='Create meteogram based on data from yr.no',
    install_requires=['matplotlib', 'numpy', 'scipy', 'pandas', 'requests', 'bs4']
)
