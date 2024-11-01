from setuptools import setup, find_packages
import os
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='AtlasIPEA',
    version='0.1',
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    url='https://github.com/0rakul0/AtlasIPEA',
    license='GPL-3.0',
    install_requires=[
        "qdrant-client",
        "sentence-transformers",
        "tqdm",
        "pandas",
        "beautifulsoup4",
        "pdfplumber"
    ],
    entry_points={
        "console_scripts": [
            "etl=src.etl:main",  # Certifique-se de que o ponto de entrada está correto
            "script_qdrant=src.script_qdrant:main",
        ]
    },
    author='Jefferson Silva dos Anjos',
    author_email='jefferson.ti@hotmail.com.br',
    description='Framework para extração e armazenamento de dados em Qdrant',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
