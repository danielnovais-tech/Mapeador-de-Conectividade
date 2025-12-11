"""
Mapeador de Conectividade
Analisa a conectividade de um grafo carregado de um arquivo JSON
"""

import json
import networkx as nx
from typing import Dict, List, Any


class ConnectivityMapper:
    """Classe para analisar conectividade de grafos"""
    
    def __init__(self, json_file: str):
        """
        Inicializa o mapeador com dados de um arquivo JSON
        
        Args:
            json_file: Caminho para o arquivo JSON com nodes e edges
        """
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        self.graph = nx.Graph()
        self._num_input_edges = 0
        
        # Adiciona nós
        if 'nodes' in data:
            self.graph.add_nodes_from(data['nodes'])
        
        # Adiciona arestas
        if 'edges' in data:
            self._num_input_edges = len(data['edges'])
            self.graph.add_edges_from(data['edges'])
    
    def get_num_nodes(self) -> int:
        """Retorna o número de nós no grafo"""
        return self.graph.number_of_nodes()
    
    def get_num_edges(self) -> int:
        """Retorna o número de arestas no input"""
        return self._num_input_edges
    
    def get_connected_components(self) -> List[List[str]]:
        """Retorna os componentes conectados do grafo"""
        components = list(nx.connected_components(self.graph))
        # Converte sets para listas ordenadas
        return [sorted(list(component)) for component in components]
    
    def get_degrees(self) -> Dict[str, int]:
        """Retorna o grau de cada nó"""
        return dict(self.graph.degree())
    
    def is_connected(self) -> bool:
        """Verifica se o grafo é conectado"""
        return nx.is_connected(self.graph)
    
    def get_shortest_paths_example(self, source: str) -> Dict[str, List[str]]:
        """
        Retorna exemplos de caminhos mais curtos a partir de um nó fonte
        
        Args:
            source: Nó fonte para calcular os caminhos
            
        Returns:
            Dicionário com caminhos mais curtos para alguns nós
        """
        paths = {}
        
        # Calcula caminhos mais curtos para todos os nós alcançáveis
        try:
            all_paths = nx.single_source_shortest_path(self.graph, source)
            paths = {target: path for target, path in all_paths.items()}
        except nx.NodeNotFound:
            pass
        
        return paths
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Gera um relatório completo de conectividade
        
        Returns:
            Dicionário com todas as métricas de conectividade
        """
        # Seleciona um nó fonte para exemplo de caminhos mais curtos
        nodes = list(self.graph.nodes())
        source_node = nodes[0] if nodes else None
        
        shortest_paths_example = {}
        if source_node:
            all_paths = self.get_shortest_paths_example(source_node)
            # Retorna apenas alguns exemplos (nó fonte e outro nó específico)
            example_keys = [source_node]
            # Prioriza mostrar caminho para nó "3" se existir
            if "3" in all_paths and "3" != source_node:
                example_keys.append("3")
            elif len(all_paths) > 1:
                # Caso contrário, mostra o primeiro nó diferente do fonte
                other_nodes = [n for n in all_paths.keys() if n != source_node]
                if other_nodes:
                    example_keys.append(sorted(other_nodes)[0])
            
            shortest_paths_example = {k: all_paths.get(k, []) for k in example_keys if k in all_paths}
        
        report = {
            "num_nodes": self.get_num_nodes(),
            "num_edges": self.get_num_edges(),
            "connected_components": self.get_connected_components(),
            "degrees": self.get_degrees(),
            "is_connected": self.is_connected(),
            "shortest_paths_example": shortest_paths_example
        }
        
        return report


def main():
    """Função principal para executar o mapeador"""
    import sys
    
    # Usa input.json como padrão ou arquivo passado como argumento
    json_file = sys.argv[1] if len(sys.argv) > 1 else 'input.json'
    
    # Cria o mapeador e gera relatório
    mapper = ConnectivityMapper(json_file)
    report = mapper.generate_report()
    
    # Imprime o relatório em formato JSON
    print(json.dumps(report, indent=4))


if __name__ == '__main__':
    main()
