import unittest
from unittest.mock import MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from services.livros_service import LivrosService

class TestLivrosService(unittest.TestCase):
    def setUp(self):
        self.mock_livros_repo=MagicMock()
        self.livros_service= LivrosService(self.mock_livros_repo)

        self.livro_data={
            "id":1,
            "titulo":"Livro Teste",
            "autor_id":1,
            "genero":"ficação",
            "editora_id":1,
            "Quantidade_paginas":300,
            "Quantidade_disponivel":5
        }

    def test_obter_todos_livros(self):
        self.mock_livros_repo.listar.return_value=[self.livro_data]

        livro= self.livros_service.obter_todos_livros()

        self.assertEqual(len(livro),1)
        self.assertEqual(livro[0]['titulo'], "Livro Teste")
        self.mock_livros_repo.listar.assert_called_once()

    def test_criar_novo_livro_sucesso(self):
        self.mock_livros_repo.adicionar_livro.return_value=self.livro_data

        livro_criada= self.livros_service.criar_livro(self.livro_data)

        self.assertEqual(livro_criada, self.livro_data)
        self.assertEqual(livro_criada["titulo"], "Livro Teste")
        self.mock_livros_repo.adicionar_livro.assert_called_once_with(self.livro_data)

    def test_criar_novo_livro_falha(self):
        dados_invalidos={"titulo":""}
        with self.assertRaises(ValueError) as cm:
            self.livros_service.criar_livro(dados_invalidos)
        self.assertEqual(str(cm.exception),"campos obrigatorios faltando")
        self.mock_livros_repo.adicionar_livro.assert_not_called()

if __name__=='__main__':
    unittest.main()