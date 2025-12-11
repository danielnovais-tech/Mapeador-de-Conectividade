#!/usr/bin/env python3
"""
Mapeador de Conectividade
Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.
"""

import json
import os
import networkx as nx
from typing import Dict, List, Any


def carregar_pontos(caminho_arquivo: str) -> List[Dict[str, Any]]:
    """
    Carrega dados de pontos de um arquivo JSON.
    
    Args:
        caminho_arquivo: Caminho para o arquivo JSON com os dados dos pontos
        
    Returns:
        Lista de dicionários contendo informações dos pontos
    """
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        pontos = json.load(arquivo)
    return pontos


def construir_grafo(pontos: List[Dict[str, Any]]) -> nx.Graph:
    """
    Constrói um grafo NetworkX a partir dos dados de pontos.
    
    Args:
        pontos: Lista de dicionários com informações dos pontos
        
    Returns:
        Grafo NetworkX com os pontos e suas conexões
    """
    G = nx.Graph()
    
    # Adicionar nós com seus atributos
    for ponto in pontos:
        G.add_node(
            ponto['id'],
            name=ponto['name'],
            lat=ponto['lat'],
            lon=ponto['lon']
        )
    
    # Adicionar arestas baseadas nos vizinhos
    for ponto in pontos:
        for vizinho in ponto['neighbors']:
            G.add_edge(ponto['id'], vizinho)
    
    return G


def gerar_relatorio_conectividade(G: nx.Graph) -> str:
    """
    Gera um relatório de conectividade do grafo.
    
    Args:
        G: Grafo NetworkX
        
    Returns:
        String com o relatório formatado
    """
    relatorio = []
    relatorio.append("=" * 60)
    relatorio.append("RELATÓRIO DE CONECTIVIDADE")
    relatorio.append("=" * 60)
    relatorio.append("")
    
    # Informações gerais
    relatorio.append(f"Total de pontos: {G.number_of_nodes()}")
    relatorio.append(f"Total de conexões: {G.number_of_edges()}")
    relatorio.append(f"Grafo conectado: {'Sim' if nx.is_connected(G) else 'Não'}")
    relatorio.append("")
    
    # Informações de cada ponto
    relatorio.append("DETALHES DOS PONTOS:")
    relatorio.append("-" * 60)
    
    for node_id in sorted(G.nodes()):
        node_data = G.nodes[node_id]
        vizinhos = list(G.neighbors(node_id))
        grau = G.degree(node_id)
        
        relatorio.append(f"\nID: {node_id}")
        relatorio.append(f"  Nome: {node_data['name']}")
        relatorio.append(f"  Coordenadas: ({node_data['lat']}, {node_data['lon']})")
        relatorio.append(f"  Grau (conexões): {grau}")
        relatorio.append(f"  Vizinhos: {', '.join(sorted(vizinhos))}")
    
    relatorio.append("")
    relatorio.append("-" * 60)
    
    # Análise de caminhos
    relatorio.append("\nANÁLISE DE CAMINHOS:")
    relatorio.append("-" * 60)
    
    nodes = sorted(G.nodes())
    for i, origem in enumerate(nodes):
        for destino in nodes[i+1:]:
            if nx.has_path(G, origem, destino):
                caminho = nx.shortest_path(G, origem, destino)
                distancia = len(caminho) - 1
                nome_origem = G.nodes[origem]['name']
                nome_destino = G.nodes[destino]['name']
                relatorio.append(f"\n{nome_origem} → {nome_destino}")
                relatorio.append(f"  Caminho: {' → '.join(caminho)}")
                relatorio.append(f"  Distância (saltos): {distancia}")
    
    relatorio.append("")
    relatorio.append("=" * 60)
    
    return "\n".join(relatorio)


def main():
    """
    Função principal que executa o mapeador de conectividade.
    """
    # Determinar o caminho do arquivo de dados
    script_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_dados = os.path.join(script_dir, 'data', 'pontos.json')
    
    print("Mapeador de Conectividade")
    print("=" * 60)
    print()
    
    # Carregar dados
    print(f"Carregando dados de: {caminho_dados}")
    pontos = carregar_pontos(caminho_dados)
    print(f"✓ {len(pontos)} pontos carregados")
    print()
    
    # Construir grafo
    print("Construindo grafo de conectividade...")
    grafo = construir_grafo(pontos)
    print(f"✓ Grafo construído com {grafo.number_of_nodes()} nós e {grafo.number_of_edges()} arestas")
    print()
    
    # Gerar e exibir relatório
    relatorio = gerar_relatorio_conectividade(grafo)
    print(relatorio)


if __name__ == "__main__":
    main()
