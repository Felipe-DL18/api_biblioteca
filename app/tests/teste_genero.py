import unittest 
from unittest.mock import MagicMock 

import sys 
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from services.genero_service import GeneroService

class TesteGeneroService(unittest.TestCase):
    def setUp(self):
        self.mock_genero_repo=MagicMock()
        self.genero_service= GeneroService(self.mock_genero_repo)

        self.genero_data={
            "id":1,
            "nome":"Genero Teste",
            "descricao":"negocio ai para testar o trem",
            "livros":[1,2,3]
        }

    def test_obter_todos_generos(self):
        self.mock_genero_repo.listar_todos.return_value=[self.genero_data]

        genero= self.genero_service.obter_todos_os_generos()

        self.assertEqual(len(genero),1)
        self.assertEqual(genero[0]['nome'],"Genero Teste")
        self.mock_genero_repo.listar_todos.assert_called_once()

    def test_criar_novo_genero_suesso(self):
        self.mock_genero_repo.adicionar_genero.return_value=self.genero_data

        genero_criado= self.genero_service.criar_novo_genero(self.genero_data)

        self.assertEqual(genero_criado,self.genero_data)
        self.assertEqual(genero_criado["nome"], "Genero Teste")
        self.mock_genero_repo.adicionar_genero.assert_called_once_with(self.genero_data)

    def test_criar_novo_genero_falha(self):
        dados_invalidos={"nome":""}

        with self.assertRaises(ValueError) as cm:
            self.genero_service.criar_novo_genero(dados_invalidos)
        self.assertEqual(str(cm.exception),"nome e descricao são obrigatorios")
        self.mock_genero_repo.adicionar_genero.assert_not_called()

if __name__=='__main__':
    unittest.main()
        