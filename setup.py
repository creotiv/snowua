from setuptools import setup, find_packages

setup(
    name='snowua',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'snowua=snowua.snowfall:run'
        ]
    }
)
