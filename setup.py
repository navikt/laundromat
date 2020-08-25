# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')


setup(
    name='laundromat',
    version='1.1.5',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=install_requires,
    author="Marius Dioli @ NAV IKT and Petter Sunde Nymark @ NAV IKT",
    description="Scrub personal information from text with Laundromat.",
    project_description="",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    package_data={'laundromat': ['spacy/data/*.csv']}

)
