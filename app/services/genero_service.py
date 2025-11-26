from repositories.genero_repository import GeneroRepository

class GeneroService:

    def __init__(self, genero_repository: GeneroRepository):
        self.genero_repository=genero_repository

    def obter_todos_os_generos(self):
        return self.genero_repository.listar_todos()
    
    def obter_genero_por_id(self, id):
        return self.genero_repository.buscar_por_id(id)
    
    def criar_novo_genero(self, dados_genero):
        if not dados_genero.get("nome") or not dados_genero.get("descricao"):
            raise ValueError("nome e descricao são obrigatorios")
        
        return self.genero_repository.adicionar_genero(dados_genero)
    
    def atualizar_genero_existente(self,id_genero,dados_genero):
        genero= self.genero_repository.buscar_por_id(id_genero)

        if not genero:
            return None
        return self.genero_repository.atualizar_genero(id_genero,dados_genero)
    
    def deletar_genero_existente(self,id_genero):
        genero= self.genero_repository.buscar_por_id(id_genero)

        if not genero:
            return None
        
        return self.genero_repository.deletar_genero(id_genero)