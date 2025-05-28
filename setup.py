
# setup.py
from setuptools import setup, find_packages

setup(
    name="health_cli",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'typer',
        'sqlalchemy',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'health-cli=health_cli.cli:app',
        ],
    },
)