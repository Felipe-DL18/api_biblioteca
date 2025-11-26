import unittest
from unittest.mock import MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from services.multa_service import MultaService

class TestMultaService(unittest.TestCase):
    def setUp(self):
        self.mock_multa_repo = MagicMock()
        self.multa_service = MultaService(self.mock_multa_repo)
    
    def test_calcular_multa_5_dias(self):
        resultado = self.multa_service.calcular_multa(5)
        self.assertEqual(resultado, 10.00)
    
    def test_calcular_multa_zero_dias(self):
        resultado = self.multa_service.calcular_multa(0)
        self.assertEqual(resultado, 0.0)
    
    def test_obter_multas_cliente_invalido(self):
        with self.assertRaises(ValueError):
            self.multa_service.obter_multas_cliente(0)

if __name__=='__main__':
    unittest.main()