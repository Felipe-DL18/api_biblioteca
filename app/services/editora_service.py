from repositories.editora_repository import EditoraRepository

#service de Editora
class EditoraService:
    #Injeção de dependência do repository
    def __init__(self, editora_repository:EditoraRepository):
        self.editora_repository= editora_repository

    #Obter todas as editoras
    def obter_todas_editoras(self):
        return self.editora_repository.listar_todas()
    
    #Obter editora por id
    def obter_editora_por_id(self,editora_id):
        return self.editora_repository.buscar_por_id(editora_id)
    
    #Criar editora
    def criar_editora(self, dados_editora):
        #Validação de dados obrigatórios
        if not dados_editora.get('nome') or not dados_editora.get('pais'):
            #se não tiver nome ou pais, lança erro
            raise ValueError("nome e pais são obrigatorios")
        #Adiciona a editora no repositório
        return self.editora_repository.adicionar_editora(dados_editora)
    
    #Atualizar editora
    def atualizar_editora(self, editora_id, dados_editora):
        #Busca a editora pelo id
        editora= self.editora_repository.buscar_por_id(editora_id)
        #Se não encontrar, retorna None
        if not editora:
            return None
        #Atualiza a editora no repositório
        return self.editora_repository.atualizar_editora(editora_id,dados_editora)
    
    #deletar editora
    def deletar_editora(self, editora_id):
        #Busca a editora pelo id
        editora= self.editora_repository.buscar_por_id(editora_id)
        #Se não encontrar, retorna None
        if not editora:
            return None
        #Deleta a editora no repositório
        return self.editora_repository.deletar_editora(editora_id)