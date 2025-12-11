import json
import networkx as nx
from typing import List, Dict
from models import Ponto, RelatorioConectividade


def carregar_pontos(arquivo: str) -> List[Ponto]:
    """Carrega pontos do arquivo JSON."""
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    pontos = []
    for item in dados['pontos']:
        ponto = Ponto(
            id=item['id'],
            nome=item['nome'],
            conexoes=item.get('conexoes', [])
        )
        pontos.append(ponto)
    
    return pontos


def construir_grafo(pontos: List[Ponto]) -> nx.Graph:
    """Constrói um grafo NetworkX a partir dos pontos."""
    G = nx.Graph()
    
    # Adiciona todos os nós
    for ponto in pontos:
        G.add_node(ponto.id, nome=ponto.nome)
    
    # Adiciona as arestas (conexões)
    for ponto in pontos:
        for conexao in ponto.conexoes:
            if conexao in G.nodes:
                G.add_edge(ponto.id, conexao)
    
    return G


def gerar_relatorio(G: nx.Graph) -> RelatorioConectividade:
    """Gera relatório de conectividade do grafo."""
    total_pontos = G.number_of_nodes()
    total_conexoes = G.number_of_edges()
    
    # Identifica componentes conectados
    componentes = list(nx.connected_components(G))
    componentes_conectados = len(componentes)
    
    # Identifica pontos isolados (grau 0)
    pontos_isolados = [node for node, degree in G.degree() if degree == 0]
    
    # Calcula densidade do grafo
    densidade = nx.density(G) if total_pontos > 1 else 0.0
    
    return RelatorioConectividade(
        total_pontos=total_pontos,
        total_conexoes=total_conexoes,
        componentes_conectados=componentes_conectados,
        pontos_isolados=pontos_isolados,
        densidade=densidade
    )


def salvar_relatorio(relatorio: RelatorioConectividade, arquivo: str):
    """Salva o relatório em formato JSON."""
    dados = {
        'total_pontos': relatorio.total_pontos,
        'total_conexoes': relatorio.total_conexoes,
        'componentes_conectados': relatorio.componentes_conectados,
        'pontos_isolados': relatorio.pontos_isolados,
        'densidade': relatorio.densidade
    }
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
