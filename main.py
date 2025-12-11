#!/usr/bin/env python3
"""
Mapeador de Conectividade: Analisa conectividade entre pontos carregados de JSON.
Execute: python main.py [opções]
Use --help para ver todas as opções disponíveis.
"""
import os
import argparse
import logging
from utils import load_points, build_graph, generate_report

def setup_logging(debug_mode):
    """Configura o sistema de logging baseado no modo debug."""
    level = logging.DEBUG if debug_mode else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def parse_arguments():
    """Parse e retorna os argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        description='Mapeador de Conectividade: Analisa e visualiza conectividade entre pontos de rede.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s                                    # Execução padrão
  %(prog)s --debug                            # Modo debug com saída detalhada
  %(prog)s --relatorio                        # Gera relatório automaticamente
  %(prog)s --importar custom/data.json        # Usa arquivo JSON customizado
  %(prog)s -d -r -i data/custom.json          # Combina múltiplas opções
        """
    )
    
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Ativa modo debug com saída verbose e logs detalhados'
    )
    
    parser.add_argument(
        '--relatorio', '-r',
        action='store_true',
        help='Gera relatório automaticamente sem solicitar confirmação do usuário'
    )
    
    parser.add_argument(
        '--importar', '-i',
        type=str,
        default='data/pontos.json',
        metavar='ARQUIVO',
        help='Especifica caminho customizado para arquivo JSON de entrada (padrão: data/pontos.json)'
    )
    
    parser.add_argument(
        '--arquivo', '-a',
        type=str,
        dest='importar',
        metavar='ARQUIVO',
        help='Alias para --importar: especifica arquivo de entrada'
    )
    
    return parser.parse_args()

def main():
    # Parse argumentos da linha de comando
    args = parse_arguments()
    
    # Configura logging baseado no modo debug
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    if args.debug:
        logger.debug("Modo debug ativado")
        logger.debug(f"Argumentos recebidos: debug={args.debug}, relatorio={args.relatorio}, importar={args.importar}")
    
    # Define diretórios e arquivos
    data_dir = 'data'
    json_file = args.importar  # Usa o arquivo especificado nos argumentos
    relatorios_dir = os.path.join(data_dir, 'relatorios')
    
    logger.info(f"Usando arquivo JSON: {json_file}")
    
    # Verifica se o arquivo existe
    if not os.path.exists(json_file):
        logger.error(f"Arquivo {json_file} não encontrado.")
        print(f"Erro: Arquivo {json_file} não encontrado.")
        print("Crie um arquivo JSON com o seguinte formato:")
        print('{"pontos": [{"id": "A", "nome": "Ponto A", "conexoes": ["B"]}]}')
        return
    
    # Carrega e processa
    try:
        logger.debug(f"Carregando pontos de {json_file}...")
        points = load_points(json_file)
        logger.info(f"Carregados {len(points)} pontos.")
        print(f"Carregados {len(points)} pontos.")
        
        if args.debug:
            logger.debug(f"Pontos carregados: {[p.get('id', 'N/A') for p in points]}")
        
        logger.debug("Construindo grafo de conectividade...")
        G = build_graph(points)
        logger.info(f"Grafo construído: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas.")
        print(f"Grafo construído: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas.")
        
        if args.debug:
            logger.debug(f"Nós do grafo: {list(G.nodes())}")
            logger.debug(f"Arestas do grafo: {list(G.edges())}")
        
        # Gera relatório (com ou sem prompt baseado na flag --relatorio)
        if args.relatorio:
            logger.info("Gerando relatório automaticamente (modo --relatorio)...")
            report_file = generate_report(G, relatorios_dir)
            logger.info(f"Relatório gerado em: {report_file}")
            print(f"Relatório gerado em: {report_file}")
        else:
            # Solicita confirmação do usuário
            resposta = input("\nDeseja gerar o relatório de conectividade? (s/n): ").strip().lower()
            if resposta in ['s', 'sim', 'y', 'yes']:
                logger.info("Gerando relatório...")
                report_file = generate_report(G, relatorios_dir)
                logger.info(f"Relatório gerado em: {report_file}")
                print(f"Relatório gerado em: {report_file}")
            else:
                logger.info("Geração de relatório cancelada pelo usuário.")
                print("Relatório não gerado.")
        
        logger.debug("Processamento concluído com sucesso.")
        
    except Exception as e:
        logger.error(f"Erro ao processar: {e}", exc_info=args.debug)
        print(f"Erro ao processar: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return

if __name__ == "__main__":
    main()
