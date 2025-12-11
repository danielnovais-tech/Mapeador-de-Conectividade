#!/usr/bin/env python3
"""
Mapeador de Conectividade: Analisa conectividade entre pontos carregados de JSON.
Execute: python main.py
"""
import os
from utils import load_points, build_graph, generate_report

def main():
    data_dir = 'data'
    json_file = os.path.join(data_dir, 'pontos.json')
    relatorios_dir = os.path.join(data_dir, 'relatorios')
    
    if not os.path.exists(json_file):
        print(f"Erro: Arquivo {json_file} não encontrado.")
        print("Crie um arquivo JSON com o seguinte formato:")
        print('{"pontos": [{"id": "A", "nome": "Ponto A", "conexoes": ["B"]}]}')
        return
    
    # Carrega e processa
    try:
        points = load_points(json_file)
        print(f"Carregados {len(points)} pontos.")
        
        G = build_graph(points)
        print(f"Grafo construído: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas.")
        
        report_file = generate_report(G, relatorios_dir)
        print(f"Relatório gerado em: {report_file}")
    except Exception as e:
        print(f"Erro ao processar: {e}")
        return

if __name__ == "__main__":
    main()
