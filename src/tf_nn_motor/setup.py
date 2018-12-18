#!/ust/bin/env python
## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD
from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

tf_nn_motor = generate_distutils_setup(
    packages=['/../../../include/tf_nn_motor'],
    package_dir={'': 'src'},
    )

setup(**tf_nn_motor)
