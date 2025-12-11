#!/usr/bin/env python3
"""
Mapeador de Conectividade
Carrega pontos de um JSON, constrói um grafo e gera relatório de conectividade.
"""

import json
import os
import networkx as nx
from pathlib import Path


def carregar_pontos(caminho_arquivo):
    """
    Carrega pontos de um arquivo JSON.
    
    Args:
        caminho_arquivo: Caminho para o arquivo JSON com os pontos.
        
    Returns:
        Lista de dicionários com os pontos carregados.
    """
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        pontos = json.load(f)
    return pontos


def construir_grafo(pontos):
    """
    Constrói um grafo a partir dos pontos.
    Conecta cada ponto ao próximo em sequência, formando um caminho.
    
    Args:
        pontos: Lista de pontos.
        
    Returns:
        Grafo NetworkX com os nós e arestas.
    """
    G = nx.Graph()
    
    # Adiciona nós
    for ponto in pontos:
        G.add_node(ponto['id'], nome=ponto['nome'], lat=ponto['lat'], lon=ponto['lon'])
    
    # Adiciona arestas conectando pontos em sequência
    # Para 4 pontos, cria: 1-2, 2-3, 3-4, 4-1 (formando um ciclo)
    for i in range(len(pontos)):
        ponto_atual = pontos[i]
        ponto_proximo = pontos[(i + 1) % len(pontos)]
        G.add_edge(ponto_atual['id'], ponto_proximo['id'])
    
    return G


def gerar_relatorio(grafo, caminho_saida):
    """
    Gera um relatório de conectividade do grafo em formato JSON.
    
    Args:
        grafo: Grafo NetworkX.
        caminho_saida: Caminho para salvar o relatório JSON.
    """
    # Cria o diretório se não existir
    Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)
    
    # Coleta informações do grafo
    relatorio = {
        "num_nos": grafo.number_of_nodes(),
        "num_arestas": grafo.number_of_edges(),
        "nos": [],
        "arestas": []
    }
    
    # Adiciona informações dos nós
    for no in grafo.nodes(data=True):
        relatorio["nos"].append({
            "id": no[0],
            "nome": no[1].get('nome', ''),
            "lat": no[1].get('lat', 0),
            "lon": no[1].get('lon', 0),
            "grau": grafo.degree(no[0])
        })
    
    # Adiciona informações das arestas
    for aresta in grafo.edges():
        relatorio["arestas"].append({
            "origem": aresta[0],
            "destino": aresta[1]
        })
    
    # Salva o relatório
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)


def main():
    """
    Função principal que executa o mapeador de conectividade.
    """
    # Define caminhos
    caminho_dados = 'data/pontos.json'
    caminho_relatorio = 'data/relatorios/connectivity_report.json'
    
    # Carrega os pontos
    pontos = carregar_pontos(caminho_dados)
    print(f"Carregados {len(pontos)} pontos.")
    
    # Constrói o grafo
    grafo = construir_grafo(pontos)
    print(f"Grafo construído: {grafo.number_of_nodes()} nós, {grafo.number_of_edges()} arestas.")
    
    # Gera o relatório
    gerar_relatorio(grafo, caminho_relatorio)
    print(f"Relatório gerado em: {caminho_relatorio}")


if __name__ == '__main__':
    main()
