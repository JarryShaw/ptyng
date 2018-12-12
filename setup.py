# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

try:
    import pty
except ImportError:
    print('Unsupported operating system!', file=sys.stderr)
    raise

# version string
__version__ = '0.3.0.post2'

# install requires
try:
    subprocess.check_call(['ps', 'axo', 'pid=,stat='],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    requirements = ['psutil']
else:
    requirements = None

# README
with open('README.rst', 'rb') as file:
    long_desc = file.read().decode('utf-8')

# set-up script for pip distribution
setup(
    name='ptyng',
    version=__version__,
    author='Jarry Shaw',
    author_email='jarryshaw@icloud.com',
    url='https://github.com/JarryShaw/ptyng',
    license='Python Software Foundation License',
    description='Pseudo-terminal utilities.',
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        ':python_version <= "3.4"': ['subprocess32>=3.5.3'],
    },
    py_modules=['ptyng'],
    package_data={
        '': [
            'LICENSE',
            'README.md',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Terminals',
    ]
)
