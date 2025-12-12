#!/usr/bin/env python3
"""
CLI para geração de relatórios personalizados.
Execute: python gerar_relatorio_cli.py
"""
import os
import sys
from relatorios import GeradorRelatorios
from utils import load_points, calcular_estatisticas_velocidade

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""


def main():
    """Função principal do CLI."""
    print(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}MAPEADOR DE CONECTIVIDADE RURAL{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
    
    # Verificar se arquivo de dados existe
    data_dir = 'data'
    json_file = os.path.join(data_dir, 'pontos.json')
    
    if not os.path.exists(json_file):
        print(f"{Fore.RED}❌ Erro: Arquivo {json_file} não encontrado.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Crie o arquivo com dados de pontos de acesso.{Style.RESET_ALL}")
        return 1
    
    try:
        # Carregar pontos
        print(f"{Fore.BLUE}📂 Carregando dados de {json_file}...{Style.RESET_ALL}")
        pontos = load_points(json_file)
        print(f"{Fore.GREEN}✅ {len(pontos)} ponto(s) carregado(s){Style.RESET_ALL}\n")
        
        if not pontos:
            print(f"{Fore.YELLOW}⚠️  Nenhum ponto encontrado no arquivo.{Style.RESET_ALL}")
            return 1
        
        # Calcular estatísticas
        print(f"{Fore.BLUE}📊 Calculando estatísticas...{Style.RESET_ALL}")
        stats = calcular_estatisticas_velocidade(pontos)
        print(f"{Fore.GREEN}✅ Estatísticas calculadas{Style.RESET_ALL}\n")
        
        # Menu de opções
        print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}OPÇÕES DE RELATÓRIO{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
        
        print("Escolha o tipo de relatório:")
        print(f"{Fore.WHITE}1. 📄 Relatório Completo (TXT){Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. 📊 Relatório Completo (JSON){Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. 🌐 Relatório Completo (HTML){Style.RESET_ALL}")
        print(f"{Fore.WHITE}4. 📈 Relatório Completo (CSV){Style.RESET_ALL}")
        print(f"{Fore.WHITE}5. ⚙️  Relatório Personalizado (Interativo){Style.RESET_ALL}")
        print(f"{Fore.WHITE}6. 🎯 Relatório de Todos os Formatos{Style.RESET_ALL}")
        print(f"{Fore.WHITE}0. 🚪 Sair{Style.RESET_ALL}")
        
        opcao = input(f"\n{Fore.GREEN}Digite sua escolha (0-6): {Style.RESET_ALL}").strip()
        
        # Criar gerador de relatórios
        gerador = GeradorRelatorios()
        
        if opcao == '1':
            print(f"\n{Fore.BLUE}📝 Gerando relatório TXT...{Style.RESET_ALL}")
            arquivo = gerador.gerar_relatorio_txt(pontos, stats)
            print(f"{Fore.GREEN}✅ Relatório TXT gerado: {arquivo}{Style.RESET_ALL}\n")
        
        elif opcao == '2':
            print(f"\n{Fore.BLUE}📝 Gerando relatório JSON...{Style.RESET_ALL}")
            arquivo = gerador.gerar_relatorio_json(pontos, stats)
            print(f"{Fore.GREEN}✅ Relatório JSON gerado: {arquivo}{Style.RESET_ALL}\n")
        
        elif opcao == '3':
            print(f"\n{Fore.BLUE}📝 Gerando relatório HTML...{Style.RESET_ALL}")
            arquivo = gerador.gerar_relatorio_html(pontos, stats)
            print(f"{Fore.GREEN}✅ Relatório HTML gerado: {arquivo}{Style.RESET_ALL}\n")
        
        elif opcao == '4':
            print(f"\n{Fore.BLUE}📝 Gerando relatório CSV...{Style.RESET_ALL}")
            arquivo = gerador.gerar_relatorio_csv(pontos, stats)
            print(f"{Fore.GREEN}✅ Relatório CSV gerado: {arquivo}{Style.RESET_ALL}\n")
        
        elif opcao == '5':
            print(f"\n{Fore.BLUE}📝 Gerando relatório personalizado...{Style.RESET_ALL}")
            arquivo = gerador.gerar_relatorio_personalizado(pontos, stats)  # Modo interativo
        
        elif opcao == '6':
            print(f"\n{Fore.BLUE}📝 Gerando relatórios em todos os formatos...{Style.RESET_ALL}")
            relatorios = gerador.gerar_relatorio_completo(pontos, stats, ['txt', 'json', 'html', 'csv'])
            print(f"{Fore.GREEN}✅ {len(relatorios)} relatório(s) gerado(s):{Style.RESET_ALL}")
            for fmt, path in relatorios.items():
                print(f"   • {fmt.upper()}: {path}")
            print()
        
        elif opcao == '0':
            print(f"\n{Fore.YELLOW}👋 Até logo!{Style.RESET_ALL}\n")
            return 0
        
        else:
            print(f"\n{Fore.RED}❌ Opção inválida. Tente novamente.{Style.RESET_ALL}\n")
            return 1
        
        return 0
    
    except FileNotFoundError as e:
        print(f"\n{Fore.RED}❌ Erro: {e}{Style.RESET_ALL}\n")
        return 1
    
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
