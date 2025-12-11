#!/usr/bin/env python3
"""
Mapeador de Conectividade
Carrega dados de pontos de um JSON, constrói um grafo com NetworkX
e gera relatórios de conectividade.
"""

import json
import os
import networkx as nx
from typing import List, Dict, Any


def carregar_pontos(caminho_arquivo: str) -> List[Dict[str, Any]]:
    """
    Carrega os dados de pontos de um arquivo JSON.
    
    Args:
        caminho_arquivo: Caminho para o arquivo JSON contendo os dados dos pontos
        
    Returns:
        Lista de dicionários com os dados dos pontos
    """
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        pontos = json.load(arquivo)
    return pontos


def construir_grafo(pontos: List[Dict[str, Any]]) -> nx.Graph:
    """
    Constrói um grafo NetworkX a partir dos dados dos pontos.
    
    Args:
        pontos: Lista de dicionários com dados dos pontos
        
    Returns:
        Grafo NetworkX com os pontos e suas conexões
    """
    grafo = nx.Graph()
    
    # Adicionar nós ao grafo com seus atributos
    for ponto in pontos:
        grafo.add_node(
            ponto['id'],
            name=ponto['name'],
            lat=ponto['lat'],
            lon=ponto['lon']
        )
    
    # Adicionar arestas (conexões) ao grafo
    for ponto in pontos:
        id_origem = ponto['id']
        for id_vizinho in ponto['neighbors']:
            # Adiciona aresta bidirecional
            grafo.add_edge(id_origem, id_vizinho)
    
    return grafo


def gerar_relatorio_conectividade(grafo: nx.Graph) -> None:
    """
    Gera e imprime um relatório de conectividade do grafo.
    
    Args:
        grafo: Grafo NetworkX a ser analisado
    """
    print("=" * 80)
    print("RELATÓRIO DE CONECTIVIDADE")
    print("=" * 80)
    print()
    
    # Informações básicas do grafo
    print(f"Número de pontos (nós): {grafo.number_of_nodes()}")
    print(f"Número de conexões (arestas): {grafo.number_of_edges()}")
    print()
    
    # Verificar se o grafo é conexo
    if nx.is_connected(grafo):
        print("✓ O grafo é CONEXO - todos os pontos estão conectados")
    else:
        print("✗ O grafo NÃO é conexo - existem componentes desconectados")
        componentes = list(nx.connected_components(grafo))
        print(f"  Número de componentes conectados: {len(componentes)}")
        for i, componente in enumerate(componentes, 1):
            print(f"  Componente {i}: {sorted(componente)}")
    print()
    
    # Informações sobre cada ponto
    print("-" * 80)
    print("DETALHES DOS PONTOS")
    print("-" * 80)
    for node_id in sorted(grafo.nodes()):
        dados = grafo.nodes[node_id]
        grau = grafo.degree(node_id)
        vizinhos = sorted(grafo.neighbors(node_id))
        
        print(f"\nPonto ID: {node_id}")
        print(f"  Nome: {dados['name']}")
        print(f"  Coordenadas: ({dados['lat']}, {dados['lon']})")
        print(f"  Grau (número de conexões): {grau}")
        print(f"  Vizinhos: {vizinhos}")
    print()
    
    # Caminhos mais curtos entre todos os pares de pontos
    print("-" * 80)
    print("CAMINHOS MAIS CURTOS")
    print("-" * 80)
    for origem in sorted(grafo.nodes()):
        for destino in sorted(grafo.nodes()):
            if origem < destino:  # Evitar duplicatas
                try:
                    caminho = nx.shortest_path(grafo, origem, destino)
                    distancia = len(caminho) - 1
                    print(f"De {origem} para {destino}: distância = {distancia}, caminho = {' → '.join(caminho)}")
                except nx.NetworkXNoPath:
                    print(f"De {origem} para {destino}: SEM CAMINHO DISPONÍVEL")
    print()
    
    # Estatísticas adicionais
    print("-" * 80)
    print("ESTATÍSTICAS ADICIONAIS")
    print("-" * 80)
    
    # Densidade do grafo
    densidade = nx.density(grafo)
    print(f"Densidade do grafo: {densidade:.4f}")
    
    # Grau médio
    graus = [grafo.degree(n) for n in grafo.nodes()]
    grau_medio = sum(graus) / len(graus)
    print(f"Grau médio dos nós: {grau_medio:.2f}")
    
    # Diâmetro (se o grafo for conexo)
    if nx.is_connected(grafo):
        diametro = nx.diameter(grafo)
        print(f"Diâmetro do grafo: {diametro}")
    
    print()
    print("=" * 80)


def main():
    """Função principal do programa."""
    # Caminho padrão para o arquivo de dados
    caminho_dados = os.path.join('data', 'pontos.json')
    
    print("Mapeador de Conectividade")
    print("-" * 80)
    print(f"Carregando dados de: {caminho_dados}")
    print()
    
    # Carregar dados dos pontos
    pontos = carregar_pontos(caminho_dados)
    print(f"✓ {len(pontos)} pontos carregados com sucesso")
    print()
    
    # Construir grafo
    grafo = construir_grafo(pontos)
    print(f"✓ Grafo construído com sucesso")
    print()
    
    # Gerar relatório de conectividade
    gerar_relatorio_conectividade(grafo)


if __name__ == '__main__':
    main()
