# -*- coding: utf-8 -*-

import shutil
import subprocess

import setuptools

PS_PATH = shutil.which('ps')
if PS_PATH is not None:
    try:
        subprocess.check_call([PS_PATH, 'axo', 'pid=,stat='],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        requirements = ['setuptools', 'psutil']
    else:
        requirements = ['setuptools']
else:
    requirements = ['setuptools']

# README
with open('./README.rst', 'r') as file:
    long_desc = file.read()

# version string
__version__ = '0.1.1'

# set-up script for pip distribution
setuptools.setup(
    name='ptyng',
    version=__version__,
    author='Jarry Shaw',
    author_email='jarryshaw@icloud.com',
    url='https://github.com/JarryShaw/ptyng',
    license='MIT License',
    description='Pseudo-terminal utilities.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    python_requires='>=3.3',
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
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
        'Topic :: Terminals',
    ]
)
