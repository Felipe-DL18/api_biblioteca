import unittest
from unittest.mock import MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from services.pagamento_service import PagamentoService

class TestPagamentoService(unittest.TestCase):
    def setUp(self):
        self.mock_pagamento_repo = MagicMock()
        self.mock_multa_repo = MagicMock()
        self.pagamento_service = PagamentoService(self.mock_pagamento_repo, self.mock_multa_repo)
    
    def test_processar_pagamento_valor_invalido(self):
        with self.assertRaises(ValueError):
            self.pagamento_service.processar_pagamento(1, 1, -10, 'PIX')
    
    def test_processar_pagamento_metodo_invalido(self):
        with self.assertRaises(ValueError):
            self.pagamento_service.processar_pagamento(1, 1, 10.0, 'Bitcoin')

if __name__=='__main__':
    unittest.main()