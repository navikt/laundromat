# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

with open('VERSION') as f:
    version = f.read()


setup(
    name='nav-pii-anon',
    version=version,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=install_requires,
    author="NAV IKT",
    description="NAV sommerstudenter anonymiserings pakke ",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    package_data={'nav_pii_anon': ['spacy/data/*.csv']}

)