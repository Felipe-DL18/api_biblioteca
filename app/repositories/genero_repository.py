from models.genero import Genero
from config.db_config import db

class GeneroRepository:
    def listar_todos(self):
        genero= Genero.query.all()
        return [g.to_dict() for g in genero]

    def buscar_por_id(self, id):
        genero= Genero.query.get(id)
        return genero.to_dict() if genero else None
    
    def adicionar_genero(self, dados_genero):
        novo_genero= Genero(
            nome=dados_genero['nome'],
            descricao=dados_genero['descricao']
        )

        db.session.add(novo_genero)
        db.session.commit()
        return novo_genero.to_dict()

    def atualizar_genero(self,id,dados_genero):
        genero= Genero.query.get(id)

        if genero:
            genero.nome= dados_genero.get("nome", genero.nome)
            genero.descricao= dados_genero.get("descricao", genero.descricao)

            db.session.commit()
            return genero.to_dict()
        
    def deletar_genero(self,id):
        genero= Genero.query.get(id)    
        if genero:
            db.session.delete(genero)
            db.session.commit()
            return True
        return False