from setuptools import find_packages, setup

setup(
    name="monitor_server",
    packages=find_packages(),
    entry_points={"console_scripts": ["monitor_server=monitor_server.main:main"]},
)
