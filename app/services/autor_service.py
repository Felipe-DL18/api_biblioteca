from repositories.autor_repository import AutorRepository

class AutorService:
    def __init__(self, autor_repository: AutorRepository):
        self.autor_repository= autor_repository

    def obter_todos_autores(self):
        return self.autor_repository.listar_todos()
    
    def obter_autor_por_id(self, autor_id):
        return self.autor_repository.buscar_por_id(autor_id)
    
    def criar_autor(self, dados_autor):
        if not dados_autor.get('nome') or not dados_autor.get('nacionalidade'):
           raise ValueError("nome e nacionalidade são obrigatorios")
        return self.autor_repository.adicionar_autor(dados_autor)
    
    def atualizar_autor(self, autor_id, dados_autor):
        autor= self.autor_repository.buscar_por_id(autor_id)
        if not autor:
            return None
        return self.autor_repository.atualizar_autor(autor_id,dados_autor)
    
    def deletar_autor(self, autor_id):
        autor= self.autor_repository.buscar_por_id(autor_id)
        if not autor:
            return None
        return self.autor_repository.deletar_autor(autor_id)            