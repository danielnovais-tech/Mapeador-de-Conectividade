from dataclasses import dataclass
from typing import List

@dataclass
class Point:
    id: str
    name: str
    lat: float
    lon: float
    neighbors: List[str]  # IDs dos vizinhos conectados
