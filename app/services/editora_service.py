from repositories.editora_repository import EditoraRepository

class EditoraService:
    def __init__(self, editora_repository:EditoraRepository):
        self.editora_repository= editora_repository

    def obter_todas_editoras(self):
        return self.editora_repository.listar_todas()
    
    def obter_editora_por_id(self,editora_id):
        return self.editora_repository.buscar_por_id(editora_id)
    
    def criar_editora(self, dados_editora):
        if not dados_editora.get('nome') or not dados_editora.get('pais'):
            raise ValueError("nome e pais são obrigatorios")
        return self.editora_repository.adicionar_editora(dados_editora)
    
    def atualizar_editora(self, editora_id, dados_editora):
        editora= self.editora_repository.buscar_por_id(editora_id)
        if not editora:
            return None
        return self.editora_repository.atualizar_editora(editora_id,dados_editora)
    
    def deletar_editora(self, editora_id):
        editora= self.editora_repository.buscar_por_id(editora_id)
        if not editora:
            return None
        return self.editora_repository.deletar_editora(editora_id)