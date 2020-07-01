# -*- coding: utf-8 -*-
import setuptools


with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

with open('VERSION') as f:
    version = f.read()


setuptools.setup(
    name='nav-pii-anon',
    version=version,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=install_requires,
    author="NAV IKT",
    description="NAV sommerstudeneter anonymiserings pakke ",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)