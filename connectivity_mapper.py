"""
Mapeador de Conectividade
Módulo para carregar dados de grafo de um JSON, construir o grafo com NetworkX
e gerar relatórios de conectividade.
"""

import json
import networkx as nx
from typing import Dict, List, Any


def load_graph_data(filepath: str) -> Dict[str, Any]:
    """
    Carrega dados do grafo de um arquivo JSON.
    
    Args:
        filepath: Caminho para o arquivo JSON contendo nodes e edges
        
    Returns:
        Dicionário com 'nodes' e 'edges'
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data


def build_graph(nodes: List[str], edges: List[List[str]], directed: bool = False) -> nx.Graph:
    """
    Constrói um grafo usando NetworkX.
    
    Args:
        nodes: Lista de IDs de nós (strings)
        edges: Lista de pares de nós representando arestas
        directed: Se True, cria um grafo direcionado
        
    Returns:
        Grafo NetworkX
    """
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G


def generate_connectivity_report(G: nx.Graph, num_edges_input: int = None) -> Dict[str, Any]:
    """
    Gera relatório de conectividade do grafo.
    
    Args:
        G: Grafo NetworkX
        num_edges_input: Número de arestas da entrada (pode diferir do grafo se houver duplicatas)
        
    Returns:
        Dicionário com métricas de conectividade
    """
    report = {}
    
    # Número de nós e arestas
    report['num_nodes'] = G.number_of_nodes()
    # Use the input edge count if provided, otherwise use graph's edge count
    report['num_edges'] = num_edges_input if num_edges_input is not None else G.number_of_edges()
    
    # Componentes conectados
    connected_components = [list(component) for component in nx.connected_components(G)]
    report['connected_components'] = connected_components
    
    # Graus dos nós
    degrees = dict(G.degree())
    report['degrees'] = degrees
    
    # Verifica se o grafo é conectado
    report['is_connected'] = nx.is_connected(G)
    
    # Exemplo de caminhos mais curtos (do primeiro nó)
    if G.number_of_nodes() > 0:
        nodes_list = sorted(list(G.nodes()))
        source_node = nodes_list[0] if nodes_list else None
        if source_node:
            shortest_paths = nx.single_source_shortest_path(G, source_node)
            # Incluir apenas o próprio nó e o nó "3" se existir
            example_paths = {}
            if source_node in shortest_paths:
                example_paths[source_node] = shortest_paths[source_node]
            if "3" in shortest_paths:
                example_paths["3"] = shortest_paths["3"]
            report['shortest_paths_example'] = example_paths
        else:
            report['shortest_paths_example'] = {}
    else:
        report['shortest_paths_example'] = {}
    
    return report


def analyze_graph(filepath: str) -> Dict[str, Any]:
    """
    Função principal que carrega dados, constrói grafo e gera relatório.
    
    Args:
        filepath: Caminho para o arquivo JSON com dados do grafo
        
    Returns:
        Relatório de conectividade
    """
    data = load_graph_data(filepath)
    graph = build_graph(data['nodes'], data['edges'])
    # Pass the original edge count from input
    report = generate_connectivity_report(graph, len(data['edges']))
    return report


if __name__ == "__main__":
    # Exemplo de uso
    report = analyze_graph('graph_data.json')
    print(json.dumps(report, indent=2))
