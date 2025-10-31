from repositories.livros_repository import LivrosRepository

class LivrosService:
    def __init__(self, livros_repository: LivrosRepository):
        self.livros_repository= livros_repository

    def obter_todos_livros(self):
        return self.livros_repository.listar()
    
    def obter_por_id(self, id_livro):
        return self.livros_repository.obter_por_id(id_livro)
    
    def criar_livro(self, dados_livro):
        if not dados_livro.get('titulo') or not dados_livro.get('editora_id') or not dados_livro.get('genero') or not dados_livro.get('autor_id'):
            raise ValueError("campos obrigatorios faltando")
        return self.livros_repository.adicionar_livro(dados_livro)
    
    def atualizar_livro(self, id_livro, dados_livro):
        livro= self.livros_repository.obter_por_id(id_livro)
        if not livro:
            raise ValueError("livro não encontrado")
        return self.livros_repository.atualizar_livro(id_livro, dados_livro)
    
    def deletar_livro(self, id_livro):
        livro= self.livros_repository.obter_por_id(id_livro)
        if not livro:
            raise ValueError("Livro não encontrado")
        return self.livros_repository.deletar_livro(id_livro)