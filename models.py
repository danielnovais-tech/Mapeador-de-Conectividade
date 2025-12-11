from typing import List
from dataclasses import dataclass


@dataclass
class Point:
    """Representa um ponto/nó na rede com coordenadas e conexões."""
    id: str
    name: str
    lat: float
    lon: float
    neighbors: List[str]
