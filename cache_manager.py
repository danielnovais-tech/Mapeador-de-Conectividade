"""Sistema de cache para construção de grafos."""
import hashlib
import json
import logging
from typing import List
import networkx as nx
from models import Point


class CachedGraphBuilder:
    """Gerenciador de cache para construção de grafos."""
    
    def __init__(self):
        self.cache = {}
    
    def build_graph(self, points: List[Point]) -> nx.Graph:
        """Constrói grafo com cache."""
        cache_key = hashlib.md5(
            json.dumps([{"id": p.id, "name": p.name, "lat": p.lat, "lon": p.lon, "neighbors": p.neighbors} 
                       for p in points], sort_keys=True).encode()
        ).hexdigest()
        
        if cache_key in self.cache:
            print("📦 Grafo recuperado do cache")
            logging.info("📦 Grafo recuperado do cache")
            return self.cache[cache_key]
        
        G = nx.Graph()
        for p in points:
            G.add_node(p.id, name=p.name, lat=p.lat, lon=p.lon)
        for p in points:
            for neighbor_id in p.neighbors:
                if G.has_node(neighbor_id):
                    G.add_edge(p.id, neighbor_id)
        
        self.cache[cache_key] = G
        print(f"✨ Grafo construído e armazenado no cache ({len(self.cache)} entradas)")
        logging.info(f"✨ Grafo construído e armazenado no cache ({len(self.cache)} entradas)")
        return G
    
    def clear_cache(self):
        """Limpa o cache."""
        self.cache.clear()
        print("🧹 Cache limpo")
        logging.info("🧹 Cache limpo")
