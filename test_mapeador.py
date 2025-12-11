"""
Testes para o Mapeador de Conectividade
"""

import json
import os
import tempfile
import unittest
from mapeador import ConnectivityMapper


class TestConnectivityMapper(unittest.TestCase):
    """Testes para a classe ConnectivityMapper"""
    
    def setUp(self):
        """Cria um arquivo temporário com dados de teste"""
        self.test_data = {
            "nodes": ["1", "2", "3", "4"],
            "edges": [
                ["1", "2"],
                ["1", "3"],
                ["3", "4"],
                ["2", "1"]
            ]
        }
        
        # Cria arquivo temporário
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()
        
        # Inicializa o mapeador
        self.mapper = ConnectivityMapper(self.temp_file.name)
    
    def tearDown(self):
        """Remove o arquivo temporário"""
        os.unlink(self.temp_file.name)
    
    def test_num_nodes(self):
        """Testa se o número de nós está correto"""
        self.assertEqual(self.mapper.get_num_nodes(), 4)
    
    def test_num_edges(self):
        """Testa se o número de arestas está correto"""
        self.assertEqual(self.mapper.get_num_edges(), 4)
    
    def test_connected_components(self):
        """Testa se os componentes conectados estão corretos"""
        components = self.mapper.get_connected_components()
        self.assertEqual(len(components), 1)
        self.assertEqual(sorted(components[0]), ["1", "2", "3", "4"])
    
    def test_degrees(self):
        """Testa se os graus dos nós estão corretos"""
        degrees = self.mapper.get_degrees()
        expected_degrees = {"1": 2, "2": 1, "3": 2, "4": 1}
        self.assertEqual(degrees, expected_degrees)
    
    def test_is_connected(self):
        """Testa se o grafo é detectado como conectado"""
        self.assertTrue(self.mapper.is_connected())
    
    def test_shortest_paths_example(self):
        """Testa os caminhos mais curtos de exemplo"""
        paths = self.mapper.get_shortest_paths_example("1")
        self.assertIn("1", paths)
        self.assertEqual(paths["1"], ["1"])
        self.assertIn("3", paths)
        self.assertEqual(paths["3"], ["1", "3"])
    
    def test_generate_report(self):
        """Testa a geração do relatório completo"""
        report = self.mapper.generate_report()
        
        # Verifica estrutura do relatório
        self.assertIn("num_nodes", report)
        self.assertIn("num_edges", report)
        self.assertIn("connected_components", report)
        self.assertIn("degrees", report)
        self.assertIn("is_connected", report)
        self.assertIn("shortest_paths_example", report)
        
        # Verifica valores esperados
        self.assertEqual(report["num_nodes"], 4)
        self.assertEqual(report["num_edges"], 4)
        self.assertEqual(report["degrees"], {"1": 2, "2": 1, "3": 2, "4": 1})
        self.assertTrue(report["is_connected"])
    
    def test_disconnected_graph(self):
        """Testa um grafo desconectado"""
        disconnected_data = {
            "nodes": ["1", "2", "3", "4"],
            "edges": [
                ["1", "2"],
                ["3", "4"]
            ]
        }
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(disconnected_data, temp_file)
        temp_file.close()
        
        try:
            mapper = ConnectivityMapper(temp_file.name)
            self.assertFalse(mapper.is_connected())
            components = mapper.get_connected_components()
            self.assertEqual(len(components), 2)
        finally:
            os.unlink(temp_file.name)


if __name__ == '__main__':
    unittest.main()
