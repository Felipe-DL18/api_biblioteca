import unittest
from unittest.mock import MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from services.emprestimos_service import EmprestimoService

class TestEmprestimoService(unittest.TestCase):
    def setUp(self):
        self.mock_emprestimo_repo=MagicMock()
        self.emprestimo_service= EmprestimoService(self.mock_emprestimo_repo)

        self.emprestimo_data={
            "id":1,
            "livro_id":1,
            "usuario_id":1,
            "data_emprestimo":"2023-10-01",
            "data_devolucao":"2023-10-15",
        }

    def test_obter_todos_emprestimos(self):
        self.mock_emprestimo_repo.listar_todos.return_value=[self.emprestimo_data]

        emprestimos= self.emprestimo_service.obter_todos_emprestimos()

        self.assertEqual(len(emprestimos),1)
        self.assertEqual(emprestimos[0]['livro_id'], 1)
        self.mock_emprestimo_repo.listar_todos.assert_called_once()

    def test_criar_novo_emprestimo_sucesso(self):
        self.mock_emprestimo_repo.adicionar_emprestimo.return_value=self.emprestimo_data

        emprestimo_criado= self.emprestimo_service.criar_emprestimo(self.emprestimo_data)

        self.assertEqual(emprestimo_criado, self.emprestimo_data)
        self.assertEqual(emprestimo_criado["livro_id"],1)
        self.mock_emprestimo_repo.adicionar_emprestimo.assert_called_once_with(self.emprestimo_data)

    def test_criar_novo_emprestimo_falha(self):
        dados_invalidos={"livro_id":""}
        with self.assertRaises(ValueError) as cm:
            self.emprestimo_service.criar_emprestimo(dados_invalidos)
        self.assertEqual(str(cm.exception),"é necessario estipular as datas de emprestimo e de devolução")
        self.mock_emprestimo_repo.adicionar_emprestimo.assert_not_called()

if __name__=='__main__':
    unittest.main()