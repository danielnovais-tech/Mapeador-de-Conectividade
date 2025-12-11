"""
Mapeador de Conectividade - Connectivity Mapper

A simple connectivity mapper for points (nodes in a network/graph),
implemented in Python. Loads point data from JSON, builds a graph
with NetworkX and generates connectivity reports.
"""

from .point import Point

__all__ = ['Point']
