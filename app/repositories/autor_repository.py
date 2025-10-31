from models.autor import Autor
from config.db_config import db

class AutorRepository:
    #buscar e mostrar todos os autrores
    def listar_todos(self):
        autor= Autor.query.all()
        return [a.to_dict() for a in autor]
    
    #buscar e mostrar um aurtor via id
    def buscar_por_id(self,id):
        autor= Autor.query.get(id)
        return autor.to_dict() if autor else None

    #adicionar um autor com os dados fornecidos   
    def adicionar_autor(self, dados_autor):
        novo_autor= Autor(
            nome= dados_autor["nome"],
            nacionalidade= dados_autor["nacionalidade"]
        )
        # Adiciona o novo autor à sessão do banco
        db.session.add(novo_autor)
        #confirma a transação no banco de dados
        db.session.commit()
        #retorna o autor criado
        return novo_autor.to_dict()
    
    #atualiza um autor existente no banco
    def atualizar_autor(self, id, dados_autor):
        #busca esse autor pelo id
        autor= Autor.query.get(id)
        #se o id for encontrado atualiza os dados
        if autor:
            #atualiza o nome se for fornecido, caso contrário mantém o valor atual
            autor.nome= dados_autor.get("nome", autor.nome)
            #faz a mesma coisa com nacionaliade
            autor.nacionalidade= dados_autor.get("nacionalidade", autor.nacionalidade)
            #comfirma as auterações no banco
            db.session.commit()
            #retorna o autor atualizado
            return autor.to_dict()
        
        #se o id não for encontrado retorna none
        return None
    
    #deleta um autor do banco
    def deletar_autor(self,id):
        #busca o autor pelo id
        autor= Autor.query.get(id)
        #se o autor for encontrado, deleta ele do banco
        if autor:
            #remove o autor da sessão do banco
            db.session.delete(autor)
            #confirma a transação no banco de dados
            db.session.commit()
            #retorna true
            return True
        #se o autor não for encontrado retorna false
        return False