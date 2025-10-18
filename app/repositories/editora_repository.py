from models.editora import Editora
from config.db_config import db

class EditoraRepository:
    def listar_todas(self):
        editoras= Editora.query.all()
        return [editora.to_dict() for editora in editoras]
    
    def buscar_por_id(self,id):
        editora= Editora.query.get(id)
        return editora.to_dict() if editora else None
    
    def adicionar_editora(self, dados_editora):
        editora=Editora(
            nome=dados_editora['nome'],
            pais=dados_editora['pais']
        )
        db.session.add(editora)
        db.session.commit()
        return editora.to_dict()
    
    def atualizar_editora(self, id, dados_editora):
        editora= Editora.query.get(id)
        if editora:
            editora.nome= dados_editora.get('nome', editora.nome)
            editora.pais= dados_editora.get('pais', editora.pais)
            db.session.commit()
            return editora.to_dict()
        return None
    
    def deletar_editora(self,id):
        editora= Editora.query.get(id)
        if editora:
            db.session.delete(editora)
            db.session.commit()
            return True
        return False