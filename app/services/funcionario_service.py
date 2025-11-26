from repositories.funcionario_repository import FuncionarioRepository

#service de Funcionario
class FuncionarioService:
    def __init__(self, funcionario_repository: FuncionarioRepository):
        self.funcionario_repository = funcionario_repository

    #Obter todos os funcionarios
    def obter_todos_funcionarios(self):
        return self.funcionario_repository.listar_funcionarios()
    
    #Obter funcionario por id
    def obter_funcionario_por_id(self, funcionario_id):
        return self.funcionario_repository.listar_por_id(funcionario_id)
    
    #Criar funcionario
    def criar_funcionario(self, dados_funcionario):
        #Validação de dados obrigatórios
        if not dados_funcionario.get('nome') or not dados_funcionario.get('CPF') or not dados_funcionario.get('email'):
            raise ValueError("Nome, CPF e email são campos obrigatórios.")
        
        #Adiciona o funcionario no repositório
        return self.funcionario_repository.adicionar_funcionario(dados_funcionario)
    
    #Atualizar funcionario
    def atualizar_funcionario(self, funcionario_id, dados_funcionario):
        #Busca o funcionario pelo id
        funcionario = self.funcionario_repository.listar_por_id(funcionario_id)

        #Se não encontrar, retorna None
        if not funcionario:
            return None
        
        #Atualiza o funcionario no repositório
        return self.funcionario_repository.atualizar_funcionario(funcionario_id, dados_funcionario)
    
    #deletar funcionario
    def deletar_funcionario(self, funcionario_id):
        #Busca o funcionario pelo id
        funcionario = self.funcionario_repository.listar_por_id(funcionario_id)

        #Se não encontrar, retorna None
        if not funcionario:
            return None
        
        #Deleta o funcionario no repositório
        return self.funcionario_repository.deletar_funcionario(funcionario_id)