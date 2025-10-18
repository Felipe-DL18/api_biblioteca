import unittest
from unittest.mock import MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from services.cliente_service import ClienteService

class TestClienteService(unittest.TestCase):
    def setUp(self):
        self.mock_cliente_repo= MagicMock()
        self.cliente_service= ClienteService(self.mock_cliente_repo)

        self.cliente_data={
            "id":1,
            "nome":"Cliente Teste",
            "email":"email@teste",
            "cpf":"12345678901",
            "status":"Permitido",
            "emprestimos":[1,2,3]
        }

    def test_obter_todos_clientes(self):
        self.mock_cliente_repo.listar_todos.return_value=[self.cliente_data]

        clietes= self.cliente_service.obter_todos_clientes()

        self.assertEqual(len(clietes),1)
        self.assertEqual(clietes[0]['nome'], "Cliente Teste")
        self.mock_cliente_repo.listar_todos.assert_called_once()

    def test_criar_novo_cliente_sucesso(self):
        self.mock_cliente_repo.adicionar_cliente.return_value=self.cliente_data

        cliente_criado= self.cliente_service.criar_cliente(self.cliente_data)

        self.assertEqual(cliente_criado, self.cliente_data)
        self.assertEqual(cliente_criado["nome"], "Cliente Teste")
        self.mock_cliente_repo.adicionar_cliente.assert_called_once_with(self.cliente_data)

    def test_criar_novo_cliente_falha(self):
        dados_invalidos={"nome":""}
        with self.assertRaises(ValueError) as cm:
            self.cliente_service.criar_cliente(dados_invalidos)
        self.assertEqual(str(cm.exception), "nome, email e cpf são obirgatorios")
        self.mock_cliente_repo.adicionar_cliente.assert_not_called()

if __name__=='__main__':
    unittest.main()