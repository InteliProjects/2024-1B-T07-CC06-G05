# Arquivo de configuração do pacote de dependências do backend
from setuptools import setup, find_packages
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './README.md')

with open(filename, "r") as readme:
    long_description = readme.read()

setup(
    name="OvO_dependencies",
    version="1.0.0",
    author="Lucas Nunes",
    author_email="lucas.nunes@sou.inteli.edu.br",
    description="Pacote de módulos próprios do grupo OvO para execução do backend.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="github.com/Inteli-College/2024-1B-T07-CC06-G05/tree/main/codigo/backend/dependencies",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)