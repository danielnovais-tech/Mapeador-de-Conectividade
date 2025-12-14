import json
import os
import logging
import networkx as nx
import matplotlib.pyplot as plt
from models import Point
from typing import List
from datetime import datetime

# Configurar logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename=f'logs/mapper_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_points(file_path: str) -> List[Point]:
    """Carrega pontos do arquivo JSON com tratamento robusto de erros."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        logging.info(f"Carregando pontos de {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("O arquivo JSON deve conter uma lista de pontos")
        
        points = [Point(**p) for p in data]
        logging.info(f"✅ {len(points)} pontos carregados com sucesso")
        return points
    except FileNotFoundError as e:
        logging.error(f"❌ Erro: {e}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"❌ Erro ao decodificar JSON: {e}")
        raise
    except Exception as e:
        logging.error(f"❌ Erro inesperado ao carregar pontos: {e}")
        raise

def build_graph(points: List[Point]) -> nx.Graph:
    """Constrói um grafo a partir dos pontos com validação de dados."""
    try:
        if not points:
            logging.warning("⚠️  Lista de pontos vazia, retornando grafo vazio")
            return nx.Graph()
        
        if not isinstance(points, list):
            raise ValueError("O parâmetro 'points' deve ser uma lista")
        
        logging.info(f"Construindo grafo com {len(points)} pontos")
        G = nx.Graph()
        
        # Adiciona nós com atributos
        for p in points:
            if not isinstance(p, Point):
                raise ValueError(f"Item inválido na lista de pontos: {p}")
            G.add_node(p.id, name=p.name, lat=p.lat, lon=p.lon)
        
        # Adiciona arestas baseadas em vizinhos
        for p in points:
            for neighbor_id in p.neighbors:
                if G.has_node(neighbor_id):  # Evita arestas inválidas
                    G.add_edge(p.id, neighbor_id)
                else:
                    logging.warning(f"⚠️  Vizinho {neighbor_id} não encontrado para o ponto {p.id}")
        
        logging.info(f"✅ Grafo construído: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")
        return G
    except Exception as e:
        logging.error(f"❌ Erro ao construir grafo: {e}")
        raise

def generate_report(G: nx.Graph, output_dir: str) -> str:
    """Gera relatório de conectividade e salva em JSON com tratamento de erros."""
    start_time = datetime.now()
    logging.info(f"Iniciando geração de relatório para grafo com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas")
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        report_file = os.path.join(output_dir, 'connectivity_report.json')
        
        # Calcula exemplo de caminho mais curto entre dois nós, se disponíveis
        shortest_path_example = []
        if len(G) >= 2:
            nodes = list(G.nodes())
            try:
                shortest_path_example = list(nx.shortest_path(G, source=nodes[0], target=nodes[-1]))
            except nx.NetworkXNoPath:
                logging.warning("⚠️  Não há caminho entre os nós de exemplo")
        
        report = {
            'num_nodes': G.number_of_nodes(),
            'num_edges': G.number_of_edges(),
            'connected_components': [list(comp) for comp in nx.connected_components(G)],
            'degrees': dict(G.degree()),
            'is_connected': nx.is_connected(G) if len(G) > 0 else False,
            'shortest_paths_example': shortest_path_example
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        logging.info(f"✅ Relatório gerado com sucesso em {elapsed:.2f}s: {report_file}")
        
        return report_file
    except PermissionError as e:
        logging.error(f"❌ Erro de permissão ao gerar relatório: {e}")
        raise
    except OSError as e:
        logging.error(f"❌ Erro de I/O ao gerar relatório: {e}")
        raise
    except Exception as e:
        logging.error(f"❌ Erro ao gerar relatório: {e}")
        raise

def visualize_graph(G: nx.Graph, output_dir: str) -> str:
    """Visualiza o grafo e salva como PNG com tratamento de erros."""
    start_time = datetime.now()
    logging.info(f"Iniciando visualização do grafo com {G.number_of_nodes()} nós")
    
    try:
        if G.number_of_nodes() == 0:
            logging.warning("⚠️  Grafo vazio, não é possível visualizar")
            raise ValueError("Grafo vazio, não é possível visualizar")
        
        os.makedirs(output_dir, exist_ok=True)
        viz_file = os.path.join(output_dir, 'graph_visualization.png')
        
        plt.figure(figsize=(10, 8))
        
        try:
            # Usa layout baseado em coordenadas geográficas (lat/lon) para posicionamento
            pos = {node: (data['lon'], data['lat']) for node, data in G.nodes(data=True)}
            
            # Valida coordenadas
            for node, (lon, lat) in pos.items():
                if not isinstance(lon, (int, float)) or not isinstance(lat, (int, float)):
                    raise ValueError(f"Coordenadas inválidas para o nó {node}: lat={lat}, lon={lon}")
            
            # Desenha o grafo
            nx.draw(G, pos, with_labels=True, labels={node: data['name'] for node, data in G.nodes(data=True)},
                    node_color='lightblue', node_size=500, font_size=10, font_weight='bold',
                    edge_color='gray')
            
            plt.title('Visualização do Grafo de Conectividade')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(viz_file, dpi=300, bbox_inches='tight')
            
            elapsed = (datetime.now() - start_time).total_seconds()
            logging.info(f"✅ Visualização gerada com sucesso em {elapsed:.2f}s: {viz_file}")
            
            return viz_file
        except KeyError as e:
            logging.error(f"❌ Erro: Nó sem coordenadas necessárias: {e}")
            raise ValueError(f"Nó sem coordenadas necessárias: {e}")
        finally:
            plt.close()
    except (IOError, OSError) as e:
        logging.error(f"❌ Erro de I/O ao salvar visualização: {e}")
        raise
    except Exception as e:
        logging.error(f"❌ Erro ao visualizar grafo: {e}")
        raise
