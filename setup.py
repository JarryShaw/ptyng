# -*- coding: utf-8 -*-


import setuptools


# README
with open('./README.rst', 'r') as file:
    long_desc = file.read()


# version string
__version__ = '0.1.0.post2'


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
    install_requires=['setuptools'],
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
