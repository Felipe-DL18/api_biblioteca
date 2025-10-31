from repositories.livros_repository import LivrosRepository

#service de Livros
class LivrosService:
    #Injeção de dependência do repository
    def __init__(self, livros_repository: LivrosRepository):
        self.livros_repository= livros_repository

    #Obter todos os livros
    def obter_todos_livros(self):
        return self.livros_repository.listar()
    
    #Obter livro por id
    def obter_por_id(self, id_livro):
        return self.livros_repository.obter_por_id(id_livro)
    
    #Criar livro
    def criar_livro(self, dados_livro):
        #Validação de dados obrigatórios
        if not dados_livro.get('titulo') or not dados_livro.get('editora_id') or not dados_livro.get('genero') or not dados_livro.get('autor_id'):
            #se não tiver titulo, editora_id, genero ou autor_id
            raise ValueError("campos obrigatorios faltando")
        #Chama o método do repository para adicionar o livro
        return self.livros_repository.adicionar_livro(dados_livro)
    
    #Atualizar livro
    def atualizar_livro(self, id_livro, dados_livro):
        #Verifica se o livro existe
        livro= self.livros_repository.obter_por_id(id_livro)
        #verifica se o livro não existe
        if not livro:
            raise ValueError("livro não encontrado")
        #Chama o método do repository para atualizar o livro
        return self.livros_repository.atualizar_livro(id_livro, dados_livro)
    
    #Deletar livro
    def deletar_livro(self, id_livro):
        #Verifica se o livro existe
        livro= self.livros_repository.obter_por_id(id_livro)
        #verifica se o livro não existe
        if not livro:
            raise ValueError("Livro não encontrado")
        #Chama o método do repository para deletar o livro
        return self.livros_repository.deletar_livro(id_livro)