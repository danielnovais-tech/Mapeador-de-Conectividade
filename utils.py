"""
Utilitários para o Mapeador de Conectividade.
Funções para carregar pontos, construir grafo e gerar relatórios.
"""
import json
import os
from datetime import datetime
import networkx as nx


def load_points(json_file):
    """
    Carrega pontos de um arquivo JSON.
    
    Args:
        json_file (str): Caminho para o arquivo JSON com os pontos.
    
    Returns:
        list: Lista de dicionários representando os pontos.
    
    Raises:
        FileNotFoundError: Se o arquivo não existe.
        json.JSONDecodeError: Se o arquivo não é um JSON válido.
        ValueError: Se o JSON não contém a chave 'pontos'.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {json_file}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao ler JSON: {e.msg}") from e
    
    if 'pontos' not in data:
        raise ValueError("O arquivo JSON deve conter uma chave 'pontos' com a lista de pontos.")
    
    return data['pontos']


def build_graph(points):
    """
    Constrói um grafo NetworkX a partir da lista de pontos.
    
    Args:
        points (list): Lista de pontos, cada um com 'id', 'nome' e 'conexoes'.
    
    Returns:
        networkx.Graph: Grafo construído com os pontos e conexões.
    """
    G = nx.Graph()
    
    # Adiciona nós
    for point in points:
        G.add_node(point['id'], nome=point.get('nome', ''))
    
    # Adiciona arestas (conexões) - apenas se ambos os nós existem
    for point in points:
        point_id = point['id']
        for connection in point.get('conexoes', []):
            # Valida que o nó de destino existe antes de criar a aresta
            if connection in G.nodes():
                G.add_edge(point_id, connection)
            else:
                print(f"Aviso: Conexão ignorada de '{point_id}' para '{connection}' (nó destino não existe)")
    
    return G


def generate_report(G, output_dir):
    """
    Gera um relatório de conectividade do grafo.
    
    Args:
        G (networkx.Graph): Grafo a ser analisado.
        output_dir (str): Diretório onde o relatório será salvo.
    
    Returns:
        str: Caminho do arquivo de relatório gerado.
    """
    # Cria o diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = os.path.join(output_dir, f'relatorio_{timestamp}.txt')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("RELATÓRIO DE CONECTIVIDADE\n")
        f.write("=" * 60 + "\n\n")
        
        # Informações básicas do grafo
        f.write(f"Total de nós: {G.number_of_nodes()}\n")
        f.write(f"Total de arestas: {G.number_of_edges()}\n\n")
        
        # Componentes conectados
        num_components = nx.number_connected_components(G)
        f.write(f"Número de componentes conectados: {num_components}\n\n")
        
        # Detalhes dos nós
        f.write("-" * 60 + "\n")
        f.write("DETALHES DOS NÓS\n")
        f.write("-" * 60 + "\n\n")
        
        for node in G.nodes():
            nome = G.nodes[node].get('nome', 'Sem nome')
            degree = G.degree(node)
            neighbors = list(G.neighbors(node))
            
            f.write(f"Nó: {node}\n")
            f.write(f"  Nome: {nome}\n")
            f.write(f"  Grau de conectividade: {degree}\n")
            f.write(f"  Conectado a: {neighbors}\n\n")
        
        # Componentes conectados detalhados
        if num_components > 1:
            f.write("-" * 60 + "\n")
            f.write("COMPONENTES CONECTADOS\n")
            f.write("-" * 60 + "\n\n")
            
            for i, component in enumerate(nx.connected_components(G), 1):
                f.write(f"Componente {i}: {list(component)}\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Relatório gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n")
    
    return report_file
