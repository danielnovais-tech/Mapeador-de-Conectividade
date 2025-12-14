#!/usr/bin/env python3
"""
Exemplo de uso do Mapeador de Conectividade.
"""
from connectivity_mapper import load_points, build_graph, generate_report, visualize_graph


def main():
    # Caminho para o arquivo de dados
    data_file = 'data/points.json'
    output_dir = 'output'
    
    print("Carregando pontos...")
    points = load_points(data_file)
    print(f"Carregados {len(points)} pontos.")
    
    print("\nConstruindo grafo...")
    G = build_graph(points)
    print(f"Grafo construído com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas.")
    
    print("\nGerando relatório de conectividade...")
    report_file = generate_report(G, output_dir)
    print(f"Relatório salvo em: {report_file}")
    
    print("\nGerando visualização do grafo...")
    viz_file = visualize_graph(G, output_dir)
    print(f"Visualização salva em: {viz_file}")
    
    print("\n✓ Processo concluído com sucesso!")


if __name__ == '__main__':
    main()
