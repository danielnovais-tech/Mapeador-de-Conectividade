"""
Funções utilitárias para o Mapeador de Conectividade.
"""
import json
import os
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt


def load_points(json_file):
    """
    Carrega pontos de um arquivo JSON.
    
    Formato esperado:
    {
        "pontos": [
            {"id": "A", "x": 0, "y": 0, "conecta": ["B", "C"]},
            {"id": "B", "x": 1, "y": 1, "conecta": ["A"]},
            ...
        ]
    }
    
    Args:
        json_file: Caminho para o arquivo JSON
        
    Returns:
        Lista de dicionários com os pontos
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('pontos', [])


def build_graph(points):
    """
    Constrói um grafo NetworkX a partir dos pontos.
    
    Args:
        points: Lista de pontos com informações de conectividade
        
    Returns:
        Grafo NetworkX
    """
    G = nx.Graph()
    
    # Adiciona nós com posições
    for point in points:
        node_id = point['id']
        x = point.get('x', 0)
        y = point.get('y', 0)
        G.add_node(node_id, pos=(x, y))
    
    # Adiciona arestas baseadas em conectividade
    for point in points:
        source = point['id']
        connections = point.get('conecta', [])
        for target in connections:
            if target in G.nodes():
                G.add_edge(source, target)
    
    return G


def generate_report(G, relatorios_dir):
    """
    Gera um relatório de conectividade do grafo.
    
    Args:
        G: Grafo NetworkX
        relatorios_dir: Diretório onde salvar o relatório
        
    Returns:
        Caminho do arquivo de relatório gerado
    """
    # Cria diretório se não existir
    os.makedirs(relatorios_dir, exist_ok=True)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = os.path.join(relatorios_dir, f'relatorio_{timestamp}.txt')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("RELATÓRIO DE CONECTIVIDADE\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("ESTATÍSTICAS GERAIS:\n")
        f.write(f"  - Número de nós: {G.number_of_nodes()}\n")
        f.write(f"  - Número de arestas: {G.number_of_edges()}\n")
        f.write(f"  - Densidade: {nx.density(G):.4f}\n")
        
        # Componentes conectados
        num_components = nx.number_connected_components(G)
        f.write(f"  - Componentes conectados: {num_components}\n\n")
        
        # Grau de cada nó
        f.write("GRAU DOS NÓS:\n")
        for node in sorted(G.nodes()):
            degree = G.degree(node)
            f.write(f"  - {node}: {degree} conexão(ões)\n")
        f.write("\n")
        
        # Componentes conectados detalhados
        if num_components > 1:
            f.write("COMPONENTES CONECTADOS:\n")
            for i, component in enumerate(nx.connected_components(G), 1):
                f.write(f"  Componente {i}: {sorted(component)}\n")
            f.write("\n")
        
        # Arestas
        f.write("CONEXÕES (ARESTAS):\n")
        for edge in sorted(G.edges()):
            f.write(f"  - {edge[0]} <-> {edge[1]}\n")
        
        f.write("\n" + "=" * 60 + "\n")
    
    return report_file


def visualize_graph(G, relatorios_dir):
    """
    Cria uma visualização do grafo e salva como imagem.
    
    Args:
        G: Grafo NetworkX
        relatorios_dir: Diretório onde salvar a visualização
        
    Returns:
        Caminho do arquivo de imagem gerado
    """
    # Cria diretório se não existir
    os.makedirs(relatorios_dir, exist_ok=True)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    viz_file = os.path.join(relatorios_dir, f'grafo_{timestamp}.png')
    
    # Configuração da figura
    plt.figure(figsize=(12, 8))
    
    # Usa as posições dos nós se disponíveis, caso contrário usa layout spring
    pos = nx.get_node_attributes(G, 'pos')
    if not pos:
        pos = nx.spring_layout(G, seed=42)
    
    # Desenha o grafo
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=700, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.6, edge_color='gray')
    
    plt.title('Mapa de Conectividade', fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    # Salva a figura
    plt.savefig(viz_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    return viz_file
