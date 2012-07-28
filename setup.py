import os
from setuptools import setup
from setuptools import find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="tasker",
    version="0.0.1",
    author="Matthias Wiesner",
    author_email="matthias.wiesner@gmail.com",
    description="Another task distribution system",
    keywords="task disrtibution",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    namespace_packages=['tasker'],
    install_requires=[
        'simplejson',
        'pyyaml',
        'pika',
        'sqlalchemy',
        'MySQL-python',
        'tornado'
    ],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.md'),
    entry_points={
        'console_scripts':[
            'manager = tasker.manager:main',
            'api = tasker.api:main',
            'initialize = tasker.manager.initialize:main'
        ],
    },
)

