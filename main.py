#!/usr/bin/env python3
"""
Script principal para testar o Mapeador de Conectividade.
"""
from connectivity_mapper import load_points, build_graph, generate_report


def main():
    """Executa o mapeador de conectividade."""
    # Carregar pontos
    print("Carregando pontos...")
    points = load_points('data/points.json')
    print(f"Carregados {len(points)} pontos.")
    
    # Construir grafo
    print("\nConstruindo grafo...")
    G = build_graph(points)
    print(f"Grafo construído com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas.")
    
    # Gerar relatório
    print("\nGerando relatório...")
    report_file = generate_report(G, 'output')
    print(f"Relatório salvo em: {report_file}")
    
    print("\n✓ Processo concluído com sucesso!")


if __name__ == '__main__':
    main()
