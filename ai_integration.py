"""Integração opcional com DeepSeek para análise de grafos com IA."""
import os
import logging
import networkx as nx
from typing import Optional

try:
    from openai import OpenAI
    DEEPSEEK_AVAILABLE = True
except ImportError:
    DEEPSEEK_AVAILABLE = False


class DeepSeekAnalyzer:
    """Analisador de grafos usando DeepSeek AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        if not DEEPSEEK_AVAILABLE:
            raise ImportError("OpenAI SDK não instalado. Execute: pip install openai")
        
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("API key não fornecida. Configure DEEPSEEK_API_KEY ou passe como parâmetro")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        )
    
    def analyze_graph(self, G: nx.Graph) -> str:
        """Analisa o grafo usando IA."""
        graph_data = {
            'num_nodes': G.number_of_nodes(),
            'num_edges': G.number_of_edges(),
            'is_connected': nx.is_connected(G) if len(G) > 0 else False,
            'degrees': dict(G.degree()),
            'density': nx.density(G)
        }
        
        prompt = f"""
Analise o seguinte grafo de conectividade:

- Número de nós: {graph_data['num_nodes']}
- Número de arestas: {graph_data['num_edges']}
- Grafo conectado: {graph_data['is_connected']}
- Densidade: {graph_data['density']:.3f}
- Graus dos nós: {graph_data['degrees']}

Forneça uma análise técnica sobre:
1. Topologia da rede
2. Pontos críticos de falha
3. Sugestões de otimização
4. Métricas de robustez
"""
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Erro ao chamar DeepSeek API: {e}")
            raise


def generate_ai_report(G: nx.Graph, output_dir: str, api_key: Optional[str] = None) -> Optional[str]:
    """Gera relatório com análise de IA (opcional)."""
    if not DEEPSEEK_AVAILABLE:
        logging.info("DeepSeek SDK não disponível. Instale com: pip install openai")
        return None
    
    try:
        analyzer = DeepSeekAnalyzer(api_key)
        analysis = analyzer.analyze_graph(G)
        
        os.makedirs(output_dir, exist_ok=True)
        report_file = os.path.join(output_dir, 'ai_connectivity_analysis.txt')
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Análise de Conectividade com IA\n\n")
            f.write(analysis)
        
        logging.info(f"✅ Relatório de IA gerado: {report_file}")
        return report_file
    except Exception as e:
        logging.warning(f"Não foi possível gerar relatório de IA: {e}")
        return None
