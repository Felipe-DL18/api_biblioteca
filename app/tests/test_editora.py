#importando bibliotecas necessarias
import unittest #importa o modulo unittest para criar testes unitarios
from unittest.mock import MagicMock #importa MagicMock para criar objetos mockados

import sys #importa o modulo sys para manipular o path do sistema
import os #importa o modulo os para manipular caminhos de arquivos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))) #adiciona o diretorio pai ao path do sistema para permitir importações relativas

from services.editora_service import EditoraService #importa a classe EditoraService do modulo editora_service

#classe de teste para o serviço de editora
class TestEditoraService(unittest.TestCase):
    #método de configuração executado antes de cada teste
    def setUp(self):
        self.mock_editora_repo=MagicMock() #cria um mock para o repositório de editoras
        self.editora_service= EditoraService(self.mock_editora_repo) #instancia o serviço de editoras com o repositório mockado
        
        #dados de exemplo para uma editora
        self.editora_data={
            "id":1,
            "nome":"Editora Teste",
            "pais":"Brasil",
            "livros":[1,2,3]
        }

    #teste para obter todas as editoras
    def test_obter_todas_editoras(self):
        #configura o mock para retornar uma lista com a editora de exemplo
        self.mock_editora_repo.listar_todas.return_value=[self.editora_data]

        #chama o método do serviço para obter todas as editoras
        editora= self.editora_service.obter_todas_editoras()

        self.assertEqual(len(editora),1) #verifica se o número de editoras retornadas é 1
        self.assertEqual(editora[0]['nome'], "Editora Teste") #verifica se o nome da editora retornada é "Editora Teste"
        self.mock_editora_repo.listar_todas.assert_called_once() #verifica se o método listar_todas do repositório foi chamado uma vez

    #teste para criar uma nova editora com sucesso
    def test_criar_nova_editora_sucesso(self):
        #configura o mock para retornar a editora de exemplo ao adicionar uma nova editora
        self.mock_editora_repo.adicionar_editora.return_value=self.editora_data

        #chama o método do serviço para criar uma nova editora
        editora_criada= self.editora_service.criar_editora(self.editora_data)

        self.assertEqual(editora_criada, self.editora_data) #verifica se a editora criada é igual à editora de exemplo
        self.assertEqual(editora_criada["nome"], "Editora Teste") #verifica se o nome da editora criada é "Editora Teste"
        self.mock_editora_repo.adicionar_editora.assert_called_once_with(self.editora_data) #verifica se o método adicionar_editora do repositório foi chamado uma vez com os dados da editora

    #teste para criar uma nova editora com falha devido a dados inválidos
    def test_criar_nova_editora_falha(self):
        #dados inválidos para a editora, faltando o nome
        dados_invalidos={"nome":""}
        #verifica se a criação da editora lança um ValueError com a mensagem correta
        with self.assertRaises(ValueError) as cm:
            self.editora_service.criar_editora(dados_invalidos)
        self.assertEqual(str(cm.exception),"nome e pais são obrigatorios") #verifica se a mensagem do erro é a esperada
        self.mock_editora_repo.adicionar_editora.assert_not_called() #verifica se o método adicionar_editora do repositório não foi chamado

# ponto de entrada para executar os testes
if __name__=='__main__':
    unittest.main()