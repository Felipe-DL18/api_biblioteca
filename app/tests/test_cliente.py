#importando bibliotecas necessarias
import unittest #importa o modulo unittest para criar testes unitarios
from unittest.mock import MagicMock #importa MagicMock para criar objetos mockados

import sys #importa o modulo sys para manipular o path do sistema
import os #importa o modulo os para manipular caminhos de arquivos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))) #adiciona o diretorio pai ao path do sistema para permitir importações relativas

from services.cliente_service import ClienteService #importa a classe ClienteService do modulo cliente_service

#classe de teste para o serviço de cliente
class TestClienteService(unittest.TestCase):
    #método de configuração executado antes de cada teste
    def setUp(self):
        self.mock_cliente_repo= MagicMock()#cria um mock para o repositório de clientes
        self.cliente_service= ClienteService(self.mock_cliente_repo)#instancia o serviço de clientes com o repositório mockado

        #dados de exemplo para um cliente
        self.cliente_data={
            "id":1,
            "nome":"Cliente Teste",
            "email":"email@teste",
            "cpf":"12345678901",
            "status":"Permitido",
            "emprestimos":[1,2,3]
        }

    #teste para obter todos os clientes
    def test_obter_todos_clientes(self):
        #configura o mock para retornar uma lista com o cliente de exemplo
        self.mock_cliente_repo.listar_todos.return_value=[self.cliente_data]

        #chama o método do serviço para obter todos os clientes
        clietes= self.cliente_service.obter_todos_clientes()

        self.assertEqual(len(clietes),1) #verifica se o número de clientes retornados é 1
        self.assertEqual(clietes[0]['nome'], "Cliente Teste") #verifica se o nome do cliente retornado é "Cliente Teste"
        self.mock_cliente_repo.listar_todos.assert_called_once() #verifica se o método listar_todos do repositório foi chamado uma vez

    #teste para criar um novo cliente com sucesso
    def test_criar_novo_cliente_sucesso(self):
        #configura o mock para retornar o cliente de exemplo ao adicionar um novo cliente
        self.mock_cliente_repo.adicionar_cliente.return_value=self.cliente_data

        #chama o método do serviço para criar um novo cliente
        cliente_criado= self.cliente_service.criar_cliente(self.cliente_data)

        self.assertEqual(cliente_criado, self.cliente_data) #verifica se o cliente criado é igual ao cliente de exemplo
        self.assertEqual(cliente_criado["nome"], "Cliente Teste") #verifica se o nome do cliente criado é "Cliente Teste"
        self.mock_cliente_repo.adicionar_cliente.assert_called_once_with(self.cliente_data) #verifica se o método adicionar_cliente do repositório foi chamado uma vez com os dados do cliente
 
    #teste para criar um novo cliente com falha devido a dados inválidos
    def test_criar_novo_cliente_falha(self):
        #dados inválidos para o cliente, faltando o nome
        dados_invalidos={"nome":""}
        #verifica se a criação do cliente lança um ValueError com a mensagem correta
        with self.assertRaises(ValueError) as cm:
            self.cliente_service.criar_cliente(dados_invalidos)
        #verifica se a mensagem do erro é a esperada
        self.assertEqual(str(cm.exception), "nome, email e cpf são obirgatorios")
        #verifica se o método adicionar_cliente do repositório não foi chamado
        self.mock_cliente_repo.adicionar_cliente.assert_not_called()

# ponto de entrada para executar os testes
if __name__=='__main__':
    unittest.main()