#!/usr/bin/python3

from setuptools import setup

setup(
        name='flaskapp',
        packages=['flaskapp'],
        include_package_data=True,
        install_requires=[
            'flask',
            ]
        )

from flask import Flask
app = Flask(__name__)



