"""
Setup configuration for Mapeador de Conectividade package.
"""

from setuptools import setup, find_packages

setup(
    name="mapeador-conectividade",
    version="0.1.0",
    description="A simple connectivity mapper for points (nodes in a network/graph)",
    author="Daniel Novais",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        # Add networkx when needed for graph functionality
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
