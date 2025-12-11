from typing import List


class Point:
    """Representa um ponto (nó) com coordenadas e vizinhos."""
    
    def __init__(self, id: str, name: str, lat: float, lon: float, neighbors: List[str] = None):
        """
        Inicializa um ponto.
        
        Args:
            id: Identificador único do ponto
            name: Nome do ponto
            lat: Latitude
            lon: Longitude
            neighbors: Lista de IDs dos pontos vizinhos
        """
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.neighbors = neighbors if neighbors is not None else []
    
    def __repr__(self):
        return f"Point(id={self.id}, name={self.name}, lat={self.lat}, lon={self.lon}, neighbors={self.neighbors})"
