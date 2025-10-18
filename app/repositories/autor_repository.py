from models.autor import Autor
from config.db_config import db

class AutorRepository:
    def listar_todos(self):
        autor= Autor.query.all()
        return [a.to_dict() for a in autor]
    
    def buscar_por_id(self,id):
        autor= Autor.query.get(id)
        return autor.to_dict() if autor else None
    
    def adicionar_autor(self, dados_autor):
        novo_autor= Autor(
            nome= dados_autor["nome"],
            nacionalidade= dados_autor["nacionalidade"]
        )
        db.session.add(novo_autor)
        db.session.commit()
        return novo_autor.to_dict()
    
    def atualizar_autor(self, id, dados_autor):
        autor= Autor.query.get(id)
        if autor:
            autor.nome= dados_autor.get("nome", autor.nome)
            autor.nacionalidade= dados_autor.get("nacionalidade", autor.nacionalidade)
            db.session.commit()
            return autor.to_dict()
        
        return None
    
    def deletar_autor(self,id):
        autor= Autor.query.get(id)
        if autor:
            db.session.delete(autor)
            db.session.commit()
            return True
        return False