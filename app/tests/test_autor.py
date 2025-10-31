#importando bibliotecas necessarias
import unittest #importa o modulo unittest para criar testes unitarios
from unittest.mock import MagicMock #importa MagicMock para criar objetos mockados

import sys #importa o modulo sys para manipular o path do sistema
import os #importa o modulo os para manipular caminhos de arquivos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))) #adiciona o diretorio pai ao path do sistema para permitir importações relativas

from services.autor_service import AutorService #importa a classe AutorService do modulo autor_service
from models.autor import Autor #importa a classe Autor do modulo autor

#classe de teste para o serviço de autor
class TestAutorService(unittest.TestCase):
    #método de configuração executado antes de cada teste
    def setUp(self):
        self.mock_autor_repo=MagicMock() #cria um mock para o repositório de autores
        self.autor_service= AutorService(self.mock_autor_repo) #instancia o serviço de autores com o repositório mockado

        #dados de exemplo para um autor
        self.autor_data={
            "id":1,
            "nome":"Teste da Silva",
            "nacionalidade":"Goiano",
            "livros":[1,2,3,4,5]
        }
    
    #teste para obter todos os autores
    def test_obter_todas(self):
        #configura o mock para retornar uma lista com o autor de exemplo
        self.mock_autor_repo.listar_todos.return_value=[self.autor_data]

        #chama o método do serviço para obter todos os autores
        autor= self.autor_service.obter_todos_autores()

        self.assertEqual(len(autor),1) #verifica se o número de autores retornadas é 1
        self.assertEqual(autor[0]['nome'],"Teste da Silva") #verifica se o nome do autor retornada é "Teste da Silva"
        self.mock_autor_repo.listar_todos.assert_called_once() #verifica se o método listar_todos do repositório foi chamado uma vez

    #teste para criar um novo autor com sucesso
    def test_crirar_novo_autor_sucesso(self):
        #configura o mock para retornar o autor de exemplo ao adicionar um novo autor
        self.mock_autor_repo.adicionar_autor.return_value=self.autor_data

        #chama o método do serviço para criar um novo autor
        autor_criado= self.autor_service.criar_autor(self.autor_data)

        self.assertEqual(autor_criado, self.autor_data) #verifica se o autor criado é igual ao autor de exemplo
        self.assertEqual(autor_criado["nome"], "Teste da Silva") #verifica se o nome do autor criado é "Teste da Silva"
        self.mock_autor_repo.adicionar_autor.assert_called_once_with(self.autor_data) #verifica se o método adicionar_autor do repositório foi chamado uma vez com os dados do autor

    #teste para criar um novo autor com falha devido a dados inválidos
    def test_criar_novo_autor_falha(self):
        #dados inválidos para o autor, faltando o nome
        dados_invalidos={"nome":""}

        #verifica se a criação do autor lança um ValueError com a mensagem correta
        with self.assertRaises(ValueError) as cm:
            self.autor_service.criar_autor(dados_invalidos)

        self.assertEqual(str(cm.exception),"nome e nacionalidade são obrigatorios")#verifica se a mensagem do erro é a esperada
        self.mock_autor_repo.adicionar_autor.assert_not_called()#verifica se o método adicionar_autor do repositório não foi chamado

# ponto de entrada para executar os testes
if __name__=='__main__':
    unittest.main()  