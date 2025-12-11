import os
from utils import carregar_pontos, construir_grafo, gerar_relatorio, salvar_relatorio


def main():
    """Função principal do mapeador de conectividade."""
    # Define caminhos
    arquivo_pontos = 'data/pontos.json'
    diretorio_relatorios = 'data/relatorios'
    arquivo_relatorio = os.path.join(diretorio_relatorios, 'connectivity_report.json')
    
    # Verifica se o arquivo de pontos existe
    if not os.path.exists(arquivo_pontos):
        print(f"Erro: Arquivo {arquivo_pontos} não encontrado.")
        print("Crie o arquivo com dados de pontos antes de executar o programa.")
        return
    
    # Cria diretório de relatórios se não existir
    os.makedirs(diretorio_relatorios, exist_ok=True)
    
    print("=== Mapeador de Conectividade ===")
    print(f"Carregando pontos de {arquivo_pontos}...")
    
    try:
        # Carrega pontos
        pontos = carregar_pontos(arquivo_pontos)
        print(f"✓ {len(pontos)} pontos carregados.")
        
        # Constrói grafo
        print("Construindo grafo...")
        grafo = construir_grafo(pontos)
        print(f"✓ Grafo construído com {grafo.number_of_nodes()} nós e {grafo.number_of_edges()} arestas.")
        
        # Gera relatório
        print("Gerando relatório de conectividade...")
        relatorio = gerar_relatorio(grafo)
        
        # Exibe resumo
        print("\n=== Resumo da Conectividade ===")
        print(f"Total de pontos: {relatorio.total_pontos}")
        print(f"Total de conexões: {relatorio.total_conexoes}")
        print(f"Componentes conectados: {relatorio.componentes_conectados}")
        print(f"Pontos isolados: {len(relatorio.pontos_isolados)}")
        if relatorio.pontos_isolados:
            print(f"  → {', '.join(relatorio.pontos_isolados)}")
        print(f"Densidade do grafo: {relatorio.densidade:.4f}")
        
        # Salva relatório
        salvar_relatorio(relatorio, arquivo_relatorio)
        print(f"\n✓ Relatório salvo em {arquivo_relatorio}")
        
    except Exception as e:
        print(f"Erro ao processar: {e}")
        return


if __name__ == '__main__':
    main()
