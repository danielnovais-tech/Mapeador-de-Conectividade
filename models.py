from dataclasses import dataclass
from typing import List


@dataclass
class Ponto:
    """Representa um ponto (nó) na rede."""
    id: str
    nome: str
    conexoes: List[str]


@dataclass
class RelatorioConectividade:
    """Relatório de conectividade da rede."""
    total_pontos: int
    total_conexoes: int
    componentes_conectados: int
    pontos_isolados: List[str]
    densidade: float
