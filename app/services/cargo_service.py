from repositories.cargo_repository import CargoRepository

#service de Cargo
class CargoService:
    #Injeção de dependência do repository
    def __init__(self, cargo_repository: CargoRepository):
        self.cargo_repository = cargo_repository

    #Obter todos os cargos
    def obter_todos_cargos(self):
        return self.cargo_repository.listar_cargos()
    
    #Obter cargo por id
    def obter_cargo_por_id(self, cargo_id):
        return self.cargo_repository.listar_por_id(cargo_id)
    
    #Criar cargo
    def criar_cargo(self, dados_cargo):
        #Validação de dados obrigatórios
        if not dados_cargo.get('cargo') or not dados_cargo.get('descricao') or not dados_cargo.get('carga_horaria_dia'):
            raise ValueError("Cargo, descrição e Carga horaria são campos obrigatórios.")
        
        #Adiciona o cargo no repositório
        return self.cargo_repository.adicionar_cargo(dados_cargo)
    
    #Atualizar cargo
    def atualizar_cargo(self, cargo_id, dados_cargo):
        #Busca o cargo pelo id
        cargo = self.cargo_repository.listar_por_id(cargo_id)

        #Se não encontrar, retorna None
        if not cargo:
            return None
        
        #Atualiza o cargo no repositório
        return self.cargo_repository.atualizar_cargo(cargo_id, dados_cargo)
    
    #deletar cargo
    def deletar_cargo(self, cargo_id):
        #Busca o cargo pelo id
        cargo = self.cargo_repository.listar_por_id(cargo_id)

        #Se não encontrar, retorna None
        if not cargo:
            return None
        
        #Deleta o cargo no repositório
        return self.cargo_repository.deletar_cargo(cargo_id)