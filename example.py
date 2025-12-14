#!/usr/bin/env python3
"""
Exemplo de uso do Mapeador de Conectividade.
"""
from connectivity_mapper import load_points, build_graph, generate_report, visualize_graph
from cache_manager import CachedGraphBuilder
from ai_integration import generate_ai_report, DEEPSEEK_AVAILABLE
import logging


def main():
    """Exemplo de uso com todas as novas funcionalidades."""
    
    # Carregar pontos
    try:
        points = load_points('data/points.json')
        print(f"✅ Carregados {len(points)} pontos")
    except Exception as e:
        print(f"❌ Erro ao carregar pontos: {e}")
        return
    
    # Construir grafo com cache
    cache_builder = CachedGraphBuilder()
    G = cache_builder.build_graph(points)
    print(f"✅ Grafo construído: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")
    
    # Gerar relatório tradicional
    try:
        report_file = generate_report(G, 'output')
        print(f"✅ Relatório gerado: {report_file}")
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
        return
    
    # Visualizar grafo
    try:
        viz_file = visualize_graph(G, 'output')
        print(f"✅ Visualização salva: {viz_file}")
    except Exception as e:
        print(f"❌ Erro ao visualizar grafo: {e}")
        return
    
    # Gerar análise com IA (se disponível)
    if DEEPSEEK_AVAILABLE:
        ai_report = generate_ai_report(G, 'output')
        if ai_report:
            print(f"✅ Análise de IA gerada: {ai_report}")
    else:
        print("ℹ️  DeepSeek não disponível. Para análise de IA, instale: pip install openai")


if __name__ == "__main__":
    main()

