import unittest
from unittest.mock import MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from services.autor_service import AutorService
from models.autor import Autor

class TestAutorService(unittest.TestCase):
    def setUp(self):
        self.mock_autor_repo=MagicMock()
        self.autor_service= AutorService(self.mock_autor_repo)

        self.autor_data={
            "id":1,
            "nome":"Teste da Silva",
            "nacionalidade":"Goiano",
            "livros":[1,2,3,4,5]
        }
    
    def test_obter_todas(self):
        self.mock_autor_repo.listar_todos.return_value=[self.autor_data]

        autor= self.autor_service.obter_todos_autores()

        self.assertEqual(len(autor),1)
        self.assertEqual(autor[0]['nome'],"Teste da Silva")
        self.mock_autor_repo.listar_todos.assert_called_once()

    def test_crirar_novo_autor_sucesso(self):
        self.mock_autor_repo.adicionar_autor.return_value=self.autor_data

        autor_criado= self.autor_service.criar_autor(self.autor_data)

        self.assertEqual(autor_criado, self.autor_data)
        self.assertEqual(autor_criado["nome"], "Teste da Silva")
        self.mock_autor_repo.adicionar_autor.assert_called_once_with(self.autor_data)

    def test_criar_novo_autor_falha(self):
        dados_invalidos={"nome":""}
        with self.assertRaises(ValueError) as cm:
            self.autor_service.criar_autor(dados_invalidos)
        self.assertEqual(str(cm.exception),"nome e nacionalidade são obrigatorios")
        self.mock_autor_repo.adicionar_autor.assert_not_called()

if __name__=='__main__':
    unittest.main()     