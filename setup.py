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
    install_requires=['matplotlib', 'numpy', 'scipy', 'pandas', 'requests', 'bs4', 'flask']
)

#
#  Packages to install on raspbian:
#  python3-matplotlib python3-numpy python3-scipy python3-pandas python3-requests python3-bs4 python3-flask
#
