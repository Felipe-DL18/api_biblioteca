#importando bibliotecas necessarias
import unittest #importa o modulo unittest para criar testes unitarios
from unittest.mock import MagicMock #importa MagicMock para criar objetos mockados

import sys #importa o modulo sys para manipular o path do sistema
import os #importa o modulo os para manipular caminhos de arquivos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))) #adiciona o diretorio pai ao path do sistema para permitir importações relativas

from services.livros_service import LivrosService #importa a classe LivrosService do modulo livros_service

#classe de teste para o serviço de livros
class TestLivrosService(unittest.TestCase):
    #método de configuração executado antes de cada teste
    def setUp(self):
        self.mock_livros_repo=MagicMock() #cria um mock para o repositório de livros
        self.livros_service= LivrosService(self.mock_livros_repo) #instancia o serviço de livros com o repositório mockado

        #dados de exemplo para um livro
        self.livro_data={
            "id":1,
            "titulo":"Livro Teste",
            "autor_id":1,
            "genero":"ficação",
            "editora_id":1,
            "Quantidade_paginas":300,
            "Quantidade_disponivel":5
        }

    #teste para obter todos os livros
    def test_obter_todos_livros(self):
        #configura o mock para retornar uma lista com o livro de exemplo
        self.mock_livros_repo.listar.return_value=[self.livro_data]

        #chama o método do serviço para obter todos os livros
        livro= self.livros_service.obter_todos_livros()

        self.assertEqual(len(livro),1) #verifica se o número de livros retornados é 1
        self.assertEqual(livro[0]['titulo'], "Livro Teste") #verifica se o título do livro retornado é "Livro Teste"
        self.mock_livros_repo.listar.assert_called_once()#verifica se o método listar do repositório foi chamado uma vez

    #teste para criar um novo livro com sucesso
    def test_criar_novo_livro_sucesso(self):
        #configura o mock para retornar o livro de exemplo ao adicionar um novo livro
        self.mock_livros_repo.adicionar_livro.return_value=self.livro_data

        #chama o método do serviço para criar um novo livro
        livro_criada= self.livros_service.criar_livro(self.livro_data)

        self.assertEqual(livro_criada, self.livro_data)#verifica se o livro criado é igual ao livro de exemplo
        self.assertEqual(livro_criada["titulo"], "Livro Teste")#verifica se o título do livro criado é "Livro Teste"
        self.mock_livros_repo.adicionar_livro.assert_called_once_with(self.livro_data)#verifica se o método adicionar_livro do repositório foi chamado uma vez com os dados do livro

    #teste para criar um novo livro com falha devido a dados inválidos
    def test_criar_novo_livro_falha(self):
        #dados inválidos para o livro, faltando o título
        dados_invalidos={"titulo":""}

        #verifica se a criação do livro lança um ValueError com a mensagem correta
        with self.assertRaises(ValueError) as cm:
            self.livros_service.criar_livro(dados_invalidos)

        #verifica se a mensagem do erro é "campos obrigatorios faltando"
        self.assertEqual(str(cm.exception),"campos obrigatorios faltando")
        #verifica se o método adicionar_livro do repositório não foi chamado
        self.mock_livros_repo.adicionar_livro.assert_not_called()

# ponto de entrada para executar os testes
if __name__=='__main__':
    unittest.main()