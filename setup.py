"""Setup configuration for Mapeador de Conectividade."""
from setuptools import setup, find_packages

setup(
    name="mapeador-conectividade",
    version="0.1.0",
    description="A simple connectivity mapper for network points",
    author="danielnovais-tech",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
