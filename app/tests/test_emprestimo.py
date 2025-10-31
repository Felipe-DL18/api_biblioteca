#importando bibliotecas necessarias
import unittest #importa o modulo unittest para criar testes unitarios
from unittest.mock import MagicMock #importa MagicMock para criar objetos mockados

import sys #importa o modulo sys para manipular o path do sistema
import os #importa o modulo os para manipular caminhos de arquivos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))) #adiciona o diretorio pai ao path do sistema para permitir importações relativas

from services.emprestimos_service import EmprestimoService #importa a classe EmprestimoService do modulo emprestimos_service

#classe de teste para o serviço de emprestimo
class TestEmprestimoService(unittest.TestCase):
    #método de configuração executado antes de cada teste
    def setUp(self):
        self.mock_emprestimo_repo=MagicMock()#cria um mock para o repositório de emprestimos
        self.emprestimo_service= EmprestimoService(self.mock_emprestimo_repo)#instancia o serviço de emprestimos com o repositório mockado

        #dados de exemplo para um emprestimo    
        self.emprestimo_data={
            "id":1,
            "livro_id":1,
            "usuario_id":1,
            "data_emprestimo":"2023-10-01",
            "data_devolucao":"2023-10-15",
        }

    #teste para obter todos os emprestimos
    def test_obter_todos_emprestimos(self):
        #configura o mock para retornar uma lista com o emprestimo de exemplo
        self.mock_emprestimo_repo.listar_todos.return_value=[self.emprestimo_data]

        #chama o método do serviço para obter todos os emprestimos
        emprestimos= self.emprestimo_service.obter_todos_emprestimos()

        self.assertEqual(len(emprestimos),1)#verifica se o número de emprestimos retornados é 1
        self.assertEqual(emprestimos[0]['livro_id'], 1)#verifica se o livro_id do emprestimo retornado é 1
        self.mock_emprestimo_repo.listar_todos.assert_called_once()#verifica se o método listar_todos do repositório foi chamado uma vez

    #teste para criar um novo emprestimo com sucesso
    def test_criar_novo_emprestimo_sucesso(self):
        #configura o mock para retornar o emprestimo de exemplo ao adicionar um novo emprestimo
        self.mock_emprestimo_repo.adicionar_emprestimo.return_value=self.emprestimo_data

        #chama o método do serviço para criar um novo emprestimo
        emprestimo_criado= self.emprestimo_service.criar_emprestimo(self.emprestimo_data)

        self.assertEqual(emprestimo_criado, self.emprestimo_data)#verifica se o emprestimo criado é igual ao emprestimo de exemplo
        self.assertEqual(emprestimo_criado["livro_id"],1)#verifica se o livro_id do emprestimo criado é 1
        self.mock_emprestimo_repo.adicionar_emprestimo.assert_called_once_with(self.emprestimo_data)#verifica se o método adicionar_emprestimo do repositório foi chamado uma vez com os dados do emprestimo

    #teste para criar um novo emprestimo com falha devido a dados inválidos
    def test_criar_novo_emprestimo_falha(self):
        #dados inválidos para o emprestimo, faltando as datas
        dados_invalidos={"livro_id":""}

        #verifica se a criação do emprestimo lança um ValueError com a mensagem correta
        with self.assertRaises(ValueError) as cm:
            self.emprestimo_service.criar_emprestimo(dados_invalidos)
        self.assertEqual(str(cm.exception),"é necessario estipular as datas de emprestimo e de devolução")#verifica se a mensagem do erro é a esperada
        self.mock_emprestimo_repo.adicionar_emprestimo.assert_not_called()#verifica se o método adicionar_emprestimo do repositório não foi chamado

# ponto de entrada para executar os testes
if __name__=='__main__':
    unittest.main()