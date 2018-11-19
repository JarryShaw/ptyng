# -*- coding: utf-8 -*-

import subprocess
import sys

try:
    import pty
except ImportError:
    print('Unsupported operating system!', file=sys.stderr)
    raise

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    subprocess.check_call(['ps', 'axo', 'pid=,stat='],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    requirements = ['setuptools', 'psutil']
else:
    requirements = list()

# README
with open('./README.rst', 'r') as file:
    long_desc = file.read()

# version string
__version__ = '0.2.0.post4'

# set-up script for pip distribution
setup(
    name='ptyng',
    version=__version__,
    author='Jarry Shaw',
    author_email='jarryshaw@icloud.com',
    url='https://github.com/JarryShaw/ptyng',
    license='MIT License',
    description='Pseudo-terminal utilities.',
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    include_package_data=True,
    install_requires=requirements,
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
        'License :: OSI Approved :: MIT License',
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
