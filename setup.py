from setuptools import setup, find_packages

REQUIRES = ['numpy', 'pandas', 'haversine', 'geopy', 'dash', 'plotly']

setup(
    name='seattlepark',
    version='0.1.0',
    packages=find_packages(),
    description="Create a parking recommender for Seattle, WA",
    requires=REQUIRES,
    python_requires='>3.7'
)
