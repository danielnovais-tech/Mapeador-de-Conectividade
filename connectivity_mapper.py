import json
import os
import networkx as nx
from models import Point
from typing import List


def load_points(file_path: str) -> List[Point]:
    """Carrega pontos do arquivo JSON."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    points = [Point(**p) for p in data]
    return points


def build_graph(points: List[Point]) -> nx.Graph:
    """Constrói um grafo a partir dos pontos."""
    G = nx.Graph()
    # Adiciona nós com atributos
    for p in points:
        G.add_node(p.id, name=p.name, lat=p.lat, lon=p.lon)
    # Adiciona arestas baseadas em vizinhos
    for p in points:
        for neighbor_id in p.neighbors:
            if G.has_node(neighbor_id):  # Evita arestas inválidas
                G.add_edge(p.id, neighbor_id)
    return G


def generate_report(G: nx.Graph, output_dir: str) -> str:
    """Gera relatório de conectividade e salva em JSON."""
    os.makedirs(output_dir, exist_ok=True)
    report_file = os.path.join(output_dir, 'connectivity_report.json')
    
    report = {
        'num_nodes': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
        'connected_components': [list(comp) for comp in nx.connected_components(G)],
        'degrees': dict(G.degree()),
        'is_connected': nx.is_connected(G) if len(G) > 0 else False,
        'shortest_paths_example': nx.shortest_path(G, source='1', target='3') if G.has_node('1') and G.has_node('3') else []
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)
    
    return report_file
