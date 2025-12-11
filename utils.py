"""
Funções utilitárias para o Mapeador de Conectividade Rural.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import networkx as nx
import matplotlib.pyplot as plt

try:
    from geopy.distance import geodesic
    GEOPY_AVAILABLE = True
except ImportError:
    GEOPY_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback to empty strings
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""


def load_points(json_file: str) -> List[Dict]:
    """
    Carrega pontos de um arquivo JSON.
    
    Suporta dois formatos:
    1. Formato simples: {"id": "A", "x": 0, "y": 0, "conecta": ["B"]}
    2. Formato completo: {"id": "PA001", "nome": "...", "latitude": ..., ...}
    
    Args:
        json_file: Caminho para o arquivo JSON
        
    Returns:
        Lista de dicionários com os pontos
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('pontos', [])


def save_points(json_file: str, points: List[Dict]) -> None:
    """
    Salva pontos em um arquivo JSON.
    
    Args:
        json_file: Caminho para o arquivo JSON
        points: Lista de dicionários com os pontos
    """
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({'pontos': points}, f, indent=2, ensure_ascii=False)


def build_graph(points: List[Dict]) -> nx.Graph:
    """
    Constrói um grafo NetworkX a partir dos pontos.
    
    Args:
        points: Lista de pontos com informações de conectividade
        
    Returns:
        Grafo NetworkX
    """
    G = nx.Graph()
    
    # Adiciona nós com posições
    for point in points:
        node_id = point['id']
        x = point.get('x', 0)
        y = point.get('y', 0)
        G.add_node(node_id, pos=(x, y))
    
    # Adiciona arestas baseadas em conectividade
    for point in points:
        source = point['id']
        connections = point.get('conecta', [])
        for target in connections:
            if target in G.nodes():
                G.add_edge(source, target)
    
    return G


def generate_report(G, relatorios_dir):
    """
    Gera um relatório de conectividade do grafo.
    
    Args:
        G: Grafo NetworkX
        relatorios_dir: Diretório onde salvar o relatório
        
    Returns:
        Caminho do arquivo de relatório gerado
    """
    # Cria diretório se não existir
    os.makedirs(relatorios_dir, exist_ok=True)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = os.path.join(relatorios_dir, f'relatorio_{timestamp}.txt')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("RELATÓRIO DE CONECTIVIDADE\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("ESTATÍSTICAS GERAIS:\n")
        f.write(f"  - Número de nós: {G.number_of_nodes()}\n")
        f.write(f"  - Número de arestas: {G.number_of_edges()}\n")
        f.write(f"  - Densidade: {nx.density(G):.4f}\n")
        
        # Componentes conectados
        num_components = nx.number_connected_components(G)
        f.write(f"  - Componentes conectados: {num_components}\n\n")
        
        # Grau de cada nó
        f.write("GRAU DOS NÓS:\n")
        for node in sorted(G.nodes()):
            degree = G.degree(node)
            f.write(f"  - {node}: {degree} conexão(ões)\n")
        f.write("\n")
        
        # Componentes conectados detalhados
        if num_components > 1:
            f.write("COMPONENTES CONECTADOS:\n")
            for i, component in enumerate(nx.connected_components(G), 1):
                f.write(f"  Componente {i}: {sorted(component)}\n")
            f.write("\n")
        
        # Arestas
        f.write("CONEXÕES (ARESTAS):\n")
        for edge in sorted(G.edges()):
            f.write(f"  - {edge[0]} <-> {edge[1]}\n")
        
        f.write("\n" + "=" * 60 + "\n")
    
    return report_file


def visualize_graph(G, relatorios_dir):
    """
    Cria uma visualização do grafo e salva como imagem.
    
    Args:
        G: Grafo NetworkX
        relatorios_dir: Diretório onde salvar a visualização
        
    Returns:
        Caminho do arquivo de imagem gerado
    """
    # Cria diretório se não existir
    os.makedirs(relatorios_dir, exist_ok=True)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    viz_file = os.path.join(relatorios_dir, f'grafo_{timestamp}.png')
    
    # Configuração da figura
    plt.figure(figsize=(12, 8))
    
    # Usa as posições dos nós se disponíveis, caso contrário usa layout spring
    pos = nx.get_node_attributes(G, 'pos')
    if not pos:
        pos = nx.spring_layout(G, seed=42)
    
    # Desenha o grafo
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=700, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.6, edge_color='gray')
    
    plt.title('Mapa de Conectividade', fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    # Salva a figura
    plt.savefig(viz_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    return viz_file


def calcular_distancia(ponto1: Dict, ponto2: Dict) -> Optional[float]:
    """
    Calcula a distância em km entre dois pontos usando coordenadas geográficas.
    
    Args:
        ponto1: Dicionário com 'latitude' e 'longitude'
        ponto2: Dicionário com 'latitude' e 'longitude'
        
    Returns:
        Distância em km ou None se geopy não estiver disponível
    """
    if not GEOPY_AVAILABLE:
        return None
    
    try:
        coord1 = (ponto1.get('latitude', 0), ponto1.get('longitude', 0))
        coord2 = (ponto2.get('latitude', 0), ponto2.get('longitude', 0))
        return geodesic(coord1, coord2).kilometers
    except Exception:
        return None


def calcular_estatisticas_velocidade(points: List[Dict]) -> Dict:
    """
    Calcula estatísticas de velocidade dos pontos.
    
    Args:
        points: Lista de pontos com dados de velocidade
        
    Returns:
        Dicionário com estatísticas (média, mediana, min, max)
    """
    velocidades_down = [p.get('velocidade_download', 0) for p in points if p.get('velocidade_download')]
    velocidades_up = [p.get('velocidade_upload', 0) for p in points if p.get('velocidade_upload')]
    latencias = [p.get('latencia', 0) for p in points if p.get('latencia')]
    
    stats = {
        'download': {
            'media': sum(velocidades_down) / len(velocidades_down) if velocidades_down else 0,
            'min': min(velocidades_down) if velocidades_down else 0,
            'max': max(velocidades_down) if velocidades_down else 0,
            'total_medições': len(velocidades_down)
        },
        'upload': {
            'media': sum(velocidades_up) / len(velocidades_up) if velocidades_up else 0,
            'min': min(velocidades_up) if velocidades_up else 0,
            'max': max(velocidades_up) if velocidades_up else 0,
            'total_medições': len(velocidades_up)
        },
        'latencia': {
            'media': sum(latencias) / len(latencias) if latencias else 0,
            'min': min(latencias) if latencias else 0,
            'max': max(latencias) if latencias else 0,
            'total_medições': len(latencias)
        }
    }
    
    return stats


def agrupar_por_comunidade(points: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Agrupa pontos por comunidade.
    
    Args:
        points: Lista de pontos
        
    Returns:
        Dicionário com comunidade como chave e lista de pontos como valor
    """
    comunidades = {}
    for point in points:
        comunidade = point.get('comunidade', 'Sem comunidade')
        if comunidade not in comunidades:
            comunidades[comunidade] = []
        comunidades[comunidade].append(point)
    return comunidades


def agrupar_por_tecnologia(points: List[Dict]) -> Dict[str, int]:
    """
    Conta pontos por tecnologia.
    
    Args:
        points: Lista de pontos
        
    Returns:
        Dicionário com tecnologia como chave e contagem como valor
    """
    tecnologias = {}
    for point in points:
        tech = point.get('tecnologia', 'Desconhecida')
        tecnologias[tech] = tecnologias.get(tech, 0) + 1
    return tecnologias


def formatar_mensagem(mensagem: str, tipo: str = 'info') -> str:
    """
    Formata mensagem com cores se colorama estiver disponível.
    
    Args:
        mensagem: Texto da mensagem
        tipo: Tipo de mensagem (info, success, warning, error)
        
    Returns:
        Mensagem formatada
    """
    if not COLORAMA_AVAILABLE:
        return mensagem
    
    cores = {
        'info': Fore.BLUE,
        'success': Fore.GREEN,
        'warning': Fore.YELLOW,
        'error': Fore.RED
    }
    
    cor = cores.get(tipo, Fore.WHITE)
    return f"{cor}{mensagem}{Style.RESET_ALL}"


def validar_ponto(point: Dict) -> Tuple[bool, Optional[str]]:
    """
    Valida se um ponto tem os campos obrigatórios.
    
    Args:
        point: Dicionário representando um ponto
        
    Returns:
        Tupla (válido, mensagem_erro)
    """
    campos_obrigatorios = ['id']
    
    for campo in campos_obrigatorios:
        if campo not in point:
            return False, f"Campo obrigatório '{campo}' não encontrado"
    
    # Verifica se tem coordenadas (x,y) ou (latitude,longitude)
    tem_coordenadas_simples = 'x' in point and 'y' in point
    tem_coordenadas_geo = 'latitude' in point and 'longitude' in point
    
    if not tem_coordenadas_simples and not tem_coordenadas_geo:
        return False, "Ponto deve ter coordenadas (x,y) ou (latitude,longitude)"
    
    return True, None


def exportar_para_csv(points: List[Dict], arquivo_csv: str) -> bool:
    """
    Exporta pontos para arquivo CSV.
    
    Args:
        points: Lista de pontos
        arquivo_csv: Caminho para o arquivo CSV
        
    Returns:
        True se exportado com sucesso, False caso contrário
    """
    if not PANDAS_AVAILABLE:
        return False
    
    try:
        df = pd.DataFrame(points)
        df.to_csv(arquivo_csv, index=False, encoding='utf-8')
        return True
    except Exception:
        return False


def importar_de_csv(arquivo_csv: str) -> List[Dict]:
    """
    Importa pontos de arquivo CSV.
    
    Args:
        arquivo_csv: Caminho para o arquivo CSV
        
    Returns:
        Lista de pontos como dicionários
    """
    if not PANDAS_AVAILABLE:
        return []
    
    try:
        df = pd.read_csv(arquivo_csv)
        return df.to_dict('records')
    except Exception:
        return []
