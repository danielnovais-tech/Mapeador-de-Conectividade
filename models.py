"""
Classes de dados para o Mapeador de Conectividade Rural.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class PontoAcesso:
    """
    Representa um ponto de acesso à internet.
    """
    id: str
    nome: str
    latitude: float
    longitude: float
    comunidade: str
    provedor: str
    tecnologia: str  # Starlink, 4G, Fibra, etc.
    velocidade_download: Optional[float] = None  # Mbps
    velocidade_upload: Optional[float] = None  # Mbps
    latencia: Optional[float] = None  # ms
    data_medicao: Optional[datetime] = None
    status: str = "ativo"  # ativo, inativo, manutencao
    observacoes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Converte o ponto de acesso para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'comunidade': self.comunidade,
            'provedor': self.provedor,
            'tecnologia': self.tecnologia,
            'velocidade_download': self.velocidade_download,
            'velocidade_upload': self.velocidade_upload,
            'latencia': self.latencia,
            'data_medicao': self.data_medicao.isoformat() if self.data_medicao else None,
            'status': self.status,
            'observacoes': self.observacoes,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PontoAcesso':
        """Cria um ponto de acesso a partir de um dicionário."""
        data = data.copy()
        if data.get('data_medicao') and isinstance(data['data_medicao'], str):
            data['data_medicao'] = datetime.fromisoformat(data['data_medicao'])
        return cls(**data)


@dataclass
class RelatorioConectividade:
    """
    Representa um relatório de conectividade.
    """
    data_geracao: datetime
    total_pontos: int
    pontos_ativos: int
    pontos_inativos: int
    velocidade_media_download: float
    velocidade_media_upload: float
    latencia_media: float
    comunidades: List[str]
    provedores: List[str]
    tecnologias: Dict[str, int]
    pontos_por_comunidade: Dict[str, int]
    estatisticas: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Converte o relatório para dicionário."""
        return {
            'data_geracao': self.data_geracao.isoformat(),
            'total_pontos': self.total_pontos,
            'pontos_ativos': self.pontos_ativos,
            'pontos_inativos': self.pontos_inativos,
            'velocidade_media_download': self.velocidade_media_download,
            'velocidade_media_upload': self.velocidade_media_upload,
            'latencia_media': self.latencia_media,
            'comunidades': self.comunidades,
            'provedores': self.provedores,
            'tecnologias': self.tecnologias,
            'pontos_por_comunidade': self.pontos_por_comunidade,
            'estatisticas': self.estatisticas
        }


@dataclass
class TesteMedicao:
    """
    Representa um teste de medição de conectividade.
    """
    ponto_id: str
    timestamp: datetime
    velocidade_download: float
    velocidade_upload: float
    latencia: float
    jitter: Optional[float] = None
    perda_pacotes: Optional[float] = None
    servidor_teste: Optional[str] = None
    sucesso: bool = True
    erro: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Converte o teste para dicionário."""
        return {
            'ponto_id': self.ponto_id,
            'timestamp': self.timestamp.isoformat(),
            'velocidade_download': self.velocidade_download,
            'velocidade_upload': self.velocidade_upload,
            'latencia': self.latencia,
            'jitter': self.jitter,
            'perda_pacotes': self.perda_pacotes,
            'servidor_teste': self.servidor_teste,
            'sucesso': self.sucesso,
            'erro': self.erro
        }
