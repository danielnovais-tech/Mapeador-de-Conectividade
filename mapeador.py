#!/usr/bin/env python3
"""
Mapeador de Conectividade
Carrega pontos de um arquivo JSON, constrói um grafo e gera relatórios de conectividade.
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path


def carregar_pontos(caminho_arquivo):
    """
    Carrega pontos de um arquivo JSON.
    
    Args:
        caminho_arquivo: Caminho para o arquivo JSON com dados dos pontos
        
    Returns:
        Lista de pontos carregados
    """
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    pontos = dados.get('pontos', [])
    print(f"Carregados {len(pontos)} pontos.")
    return pontos


def construir_grafo(pontos):
    """
    Constrói um grafo NetworkX a partir dos pontos e suas conexões.
    
    Args:
        pontos: Lista de pontos com informações de conexões
        
    Returns:
        Grafo NetworkX construído
    """
    G = nx.Graph()
    
    # Adicionar nós
    for ponto in pontos:
        G.add_node(ponto['id'], nome=ponto['nome'], x=ponto['x'], y=ponto['y'])
    
    # Adicionar arestas baseadas nas conexões
    for ponto in pontos:
        for conexao in ponto.get('conexoes', []):
            # Adicionar aresta apenas se ainda não existe (evitar duplicatas)
            if not G.has_edge(ponto['id'], conexao):
                G.add_edge(ponto['id'], conexao)
    
    num_nos = G.number_of_nodes()
    num_arestas = G.number_of_edges()
    print(f"Grafo construído: {num_nos} nós, {num_arestas} arestas.")
    
    return G


def gerar_relatorio(grafo, caminho_saida):
    """
    Gera um relatório de conectividade em formato JSON.
    
    Args:
        grafo: Grafo NetworkX
        caminho_saida: Caminho para salvar o relatório JSON
    """
    relatorio = {
        "numero_de_nos": grafo.number_of_nodes(),
        "numero_de_arestas": grafo.number_of_edges(),
        "densidade": nx.density(grafo),
        "nos": [],
        "arestas": []
    }
    
    # Informações dos nós
    for no in grafo.nodes(data=True):
        node_id, attrs = no
        relatorio["nos"].append({
            "id": node_id,
            "nome": attrs.get('nome', f'No {node_id}'),
            "grau": grafo.degree(node_id),
            "x": attrs.get('x', 0),
            "y": attrs.get('y', 0)
        })
    
    # Informações das arestas
    for aresta in grafo.edges():
        relatorio["arestas"].append({
            "origem": aresta[0],
            "destino": aresta[1]
        })
    
    # Criar diretório se não existir
    Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)
    
    # Salvar relatório
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print(f"Relatório gerado em: {caminho_saida}")


def gerar_visualizacao(grafo, caminho_saida):
    """
    Gera uma visualização do grafo em formato PNG.
    
    Args:
        grafo: Grafo NetworkX
        caminho_saida: Caminho para salvar a imagem PNG
    """
    plt.figure(figsize=(10, 8))
    
    # Obter posições dos nós baseadas nas coordenadas x, y
    pos = {}
    for no in grafo.nodes(data=True):
        node_id, attrs = no
        pos[node_id] = (attrs.get('x', 0), attrs.get('y', 0))
    
    # Desenhar o grafo
    nx.draw_networkx_nodes(grafo, pos, node_color='lightblue', 
                          node_size=700, alpha=0.9)
    nx.draw_networkx_edges(grafo, pos, width=2, alpha=0.6)
    
    # Adicionar labels com nomes dos nós
    labels = {}
    for no in grafo.nodes(data=True):
        node_id, attrs = no
        labels[node_id] = attrs.get('nome', f'Nó {node_id}')
    
    nx.draw_networkx_labels(grafo, pos, labels, font_size=10, font_weight='bold')
    
    plt.title('Grafo de Conectividade', fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    # Criar diretório se não existir
    Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)
    
    # Salvar visualização
    plt.savefig(caminho_saida, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Visualização gerada em: {caminho_saida}")


def main():
    """Função principal do mapeador de conectividade."""
    # Caminhos dos arquivos
    caminho_pontos = 'data/pontos.json'
    caminho_relatorio = 'data/relatorios/connectivity_report.json'
    caminho_visualizacao = 'data/relatorios/graph_visualization.png'
    
    # Carregar pontos
    pontos = carregar_pontos(caminho_pontos)
    
    # Construir grafo
    grafo = construir_grafo(pontos)
    
    # Gerar relatório
    gerar_relatorio(grafo, caminho_relatorio)
    
    # Gerar visualização
    gerar_visualizacao(grafo, caminho_visualizacao)


if __name__ == '__main__':
    main()
