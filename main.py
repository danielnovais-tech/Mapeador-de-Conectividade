#!/usr/bin/env python3
"""
Mapeador de Conectividade: Analisa conectividade entre pontos carregados de JSON.
Execute: python main.py
"""
import os
import json
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt


class MapeadorConectividade:
    """
    Classe principal para mapear e analisar conectividade entre pontos.
    """
    
    def __init__(self, data_dir='data'):
        """
        Inicializa o mapeador de conectividade.
        
        Args:
            data_dir: Diretório onde estão os dados e onde serão salvos os relatórios
        """
        self.data_dir = data_dir
        self.json_file = os.path.join(data_dir, 'pontos.json')
        self.relatorios_dir = os.path.join(data_dir, 'relatorios')
        self.points = []
        self.graph = None
    
    def load_points(self):
        """
        Carrega pontos de um arquivo JSON.
        
        Returns:
            Lista de dicionários com os pontos
        """
        if not os.path.exists(self.json_file):
            raise FileNotFoundError(f"Arquivo {self.json_file} não encontrado.")
        
        with open(self.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.points = data.get('pontos', [])
        return self.points
    
    def build_graph(self):
        """
        Constrói um grafo NetworkX a partir dos pontos carregados.
        
        Returns:
            Grafo NetworkX
        """
        self.graph = nx.Graph()
        
        # Adiciona nós com posições
        for point in self.points:
            node_id = point['id']
            x = point.get('x', 0)
            y = point.get('y', 0)
            self.graph.add_node(node_id, pos=(x, y))
        
        # Adiciona arestas baseadas em conectividade
        for point in self.points:
            source = point['id']
            connections = point.get('conecta', [])
            for target in connections:
                if target in self.graph.nodes():
                    self.graph.add_edge(source, target)
        
        return self.graph
    
    def generate_report(self):
        """
        Gera um relatório de conectividade do grafo.
        
        Returns:
            Caminho do arquivo de relatório gerado
        """
        if self.graph is None:
            raise ValueError("Grafo não foi construído. Execute build_graph() primeiro.")
        
        # Cria diretório se não existir
        os.makedirs(self.relatorios_dir, exist_ok=True)
        
        # Nome do arquivo com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(self.relatorios_dir, f'relatorio_{timestamp}.txt')
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("RELATÓRIO DE CONECTIVIDADE\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("ESTATÍSTICAS GERAIS:\n")
            f.write(f"  - Número de nós: {self.graph.number_of_nodes()}\n")
            f.write(f"  - Número de arestas: {self.graph.number_of_edges()}\n")
            f.write(f"  - Densidade: {nx.density(self.graph):.4f}\n")
            
            # Componentes conectados
            num_components = nx.number_connected_components(self.graph)
            f.write(f"  - Componentes conectados: {num_components}\n\n")
            
            # Grau de cada nó
            f.write("GRAU DOS NÓS:\n")
            for node in sorted(self.graph.nodes()):
                degree = self.graph.degree(node)
                f.write(f"  - {node}: {degree} conexão(ões)\n")
            f.write("\n")
            
            # Componentes conectados detalhados
            if num_components > 1:
                f.write("COMPONENTES CONECTADOS:\n")
                for i, component in enumerate(nx.connected_components(self.graph), 1):
                    f.write(f"  Componente {i}: {sorted(component)}\n")
                f.write("\n")
            
            # Arestas
            f.write("CONEXÕES (ARESTAS):\n")
            for edge in sorted(self.graph.edges()):
                f.write(f"  - {edge[0]} <-> {edge[1]}\n")
            
            f.write("\n" + "=" * 60 + "\n")
        
        return report_file
    
    def visualize_graph(self):
        """
        Cria uma visualização do grafo e salva como imagem.
        
        Returns:
            Caminho do arquivo de imagem gerado
        """
        if self.graph is None:
            raise ValueError("Grafo não foi construído. Execute build_graph() primeiro.")
        
        # Cria diretório se não existir
        os.makedirs(self.relatorios_dir, exist_ok=True)
        
        # Nome do arquivo com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        viz_file = os.path.join(self.relatorios_dir, f'grafo_{timestamp}.png')
        
        # Configuração da figura
        plt.figure(figsize=(12, 8))
        
        # Usa as posições dos nós se disponíveis, caso contrário usa layout spring
        pos = nx.get_node_attributes(self.graph, 'pos')
        if not pos:
            pos = nx.spring_layout(self.graph, seed=42)
        
        # Desenha o grafo
        nx.draw_networkx_nodes(self.graph, pos, node_color='lightblue', 
                              node_size=700, alpha=0.9)
        nx.draw_networkx_labels(self.graph, pos, font_size=12, font_weight='bold')
        nx.draw_networkx_edges(self.graph, pos, width=2, alpha=0.6, edge_color='gray')
        
        plt.title('Mapa de Conectividade', fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        # Salva a figura
        plt.savefig(viz_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        return viz_file
    
    def executar(self):
        """
        Executa o fluxo completo de análise de conectividade.
        """
        try:
            # Carrega e processa
            self.load_points()
            print(f"Carregados {len(self.points)} pontos.")
            
            self.build_graph()
            print(f"Grafo construído: {self.graph.number_of_nodes()} nós, {self.graph.number_of_edges()} arestas.")
            
            report_file = self.generate_report()
            print(f"Relatório gerado em: {report_file}")
            
            viz_file = self.visualize_graph()
            print(f"Visualização gerada em: {viz_file}")
            
        except FileNotFoundError as e:
            print(f"Erro: {e} Crie-o com dados de exemplo.")
        except Exception as e:
            print(f"Erro durante a execução: {e}")


def main():
    mapeador = MapeadorConectividade()
    mapeador.executar()


if __name__ == "__main__":
    main()
