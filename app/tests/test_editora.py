import unittest
from unittest.mock import MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from services.editora_service import EditoraService

class TestEditoraService(unittest.TestCase):
    def setUp(self):
        self.mock_editora_repo=MagicMock()
        self.editora_service= EditoraService(self.mock_editora_repo)
        self.editora_data={
            "id":1,
            "nome":"Editora Teste",
            "pais":"Brasil",
            "livros":[1,2,3]
        }

    def test_obter_todas_editoras(self):
        self.mock_editora_repo.listar_todas.return_value=[self.editora_data]

        editora= self.editora_service.obter_todas_editoras()

        self.assertEqual(len(editora),1)
        self.assertEqual(editora[0]['nome'], "Editora Teste")
        self.mock_editora_repo.listar_todas.assert_called_once()

    def test_criar_nova_editora_sucesso(self):
        self.mock_editora_repo.adicionar_editora.return_value=self.editora_data

        editora_criada= self.editora_service.criar_editora(self.editora_data)

        self.assertEqual(editora_criada, self.editora_data)
        self.assertEqual(editora_criada["nome"], "Editora Teste")
        self.mock_editora_repo.adicionar_editora.assert_called_once_with(self.editora_data)

    def test_criar_nova_editora_falha(self):
        dados_invalidos={"nome":""}
        with self.assertRaises(ValueError) as cm:
            self.editora_service.criar_editora(dados_invalidos)
        self.assertEqual(str(cm.exception),"nome e pais são obrigatorios")
        self.mock_editora_repo.adicionar_editora.assert_not_called()

if __name__=='__main__':
    unittest.main()