"""
Point dataclass for representing nodes in a connectivity network.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    """
    Represents a point/node in a connectivity network.
    
    Attributes:
        id: Unique identifier for the point
        name: Human-readable name of the point
        lat: Latitude coordinate of the point
        lon: Longitude coordinate of the point
        neighbors: List of IDs of connected neighboring points
    """
    id: str
    name: str
    lat: float
    lon: float
    neighbors: List[str]  # IDs dos vizinhos conectados
