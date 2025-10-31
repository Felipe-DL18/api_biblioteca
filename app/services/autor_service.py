from repositories.autor_repository import AutorRepository

#service de Autor
class AutorService:
    #Injeção de dependência do repository
    def __init__(self, autor_repository: AutorRepository):
        self.autor_repository= autor_repository

    #Obter todos os autores
    def obter_todos_autores(self):
        return self.autor_repository.listar_todos()
    
    #Obter autor por id
    def obter_autor_por_id(self, autor_id):
        return self.autor_repository.buscar_por_id(autor_id)
    
    #Criar autor
    def criar_autor(self, dados_autor):
        #Validação de dados obrigatórios
        if not dados_autor.get('nome') or not dados_autor.get('nacionalidade'):
           #se não tiver nome ou nacionalidade, lança erro
           raise ValueError("nome e nacionalidade são obrigatorios")
        #Adiciona o autor no repositório
        return self.autor_repository.adicionar_autor(dados_autor)
    
    #Atualizar autor
    def atualizar_autor(self, autor_id, dados_autor):
        #Busca o autor pelo id
        autor= self.autor_repository.buscar_por_id(autor_id)
        #Se não encontrar, retorna None
        if not autor:
            return None
        #Atualiza o autor no repositório
        return self.autor_repository.atualizar_autor(autor_id,dados_autor)
    
    #deletar autor
    def deletar_autor(self, autor_id):
        #Busca o autor pelo id
        autor= self.autor_repository.buscar_por_id(autor_id)
        #Se não encontrar, retorna None
        if not autor:
            return None
        #Deleta o autor no repositório
        return self.autor_repository.deletar_autor(autor_id)            