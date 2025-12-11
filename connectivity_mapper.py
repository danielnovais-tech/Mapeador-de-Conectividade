import json
import os
import networkx as nx
import matplotlib.pyplot as plt
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
    
    # Calcula exemplo de caminho mais curto entre dois nós, se disponíveis
    shortest_path_example = []
    if len(G) >= 2:
        nodes = list(G.nodes())
        shortest_path_example = list(nx.shortest_path(G, source=nodes[0], target=nodes[-1]))
    
    report = {
        'num_nodes': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
        'connected_components': [list(comp) for comp in nx.connected_components(G)],
        'degrees': dict(G.degree()),
        'is_connected': nx.is_connected(G) if len(G) > 0 else False,
        'shortest_paths_example': shortest_path_example
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)
    
    return report_file

def visualize_graph(G: nx.Graph, output_dir: str) -> str:
    """Visualiza o grafo e salva como PNG."""
    os.makedirs(output_dir, exist_ok=True)
    viz_file = os.path.join(output_dir, 'graph_visualization.png')
    
    plt.figure(figsize=(10, 8))
    
    # Usa layout baseado em coordenadas geográficas (lat/lon) para posicionamento
    pos = {node: (data['lon'], data['lat']) for node, data in G.nodes(data=True)}
    
    # Desenha o grafo
    nx.draw(G, pos, with_labels=True, labels={node: data['name'] for node, data in G.nodes(data=True)},
            node_color='lightblue', node_size=500, font_size=10, font_weight='bold',
            edge_color='gray')
    
    plt.title('Visualização do Grafo de Conectividade')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(viz_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return viz_file
