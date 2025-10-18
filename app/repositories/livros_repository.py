from models.livros import Livros
from models.autor import Autor
from models.editora import Editora
from config.db_config import db
from sqlalchemy import and_

class LivrosRepository:
    def listar(self, titulo=None, autor_nome=None, editora_nome=None, genero=None):
        query= Livros.query

        if titulo:
            query= query.filter(Livros.titulo.ilike(f"%{titulo}%"))
        if autor_nome:
            query = query.join(Autor).filter(Autor.nome.ilike(f"%{autor_nome}%"))
        if editora_nome:
            query = query.join(Editora).filter(Editora.nome.ilike(f"%{editora_nome}%"))
        if genero:
            query= query.filter(Livros.Genero.ilike(f"%{genero}%"))
        
        livros= query.order_by(Livros.titulo).all()
        return[livro.to_dict() for livro in livros]
    
    def obter_por_id(self, id):
        livro= Livros.query.get(id)
        return livro.to_dict() if livro else None
    
    def adicionar_livro(self, livro_dados):
        editora_id= livro_dados["editora_id"]
        autor_id= livro_dados["autor_id"]

        autor = Autor.query.filter_by(id_autor=autor_id).first()
        editora = Editora.query.filter_by(id_editora=editora_id).first()
        if not autor:
            autor= Autor(nome=autor_id)
            editora= Editora(nome=editora_id)
            db.session.add(autor)
            db.session.commit()

        livro= Livros(
            titulo=livro_dados["titulo"],
            Genero=livro_dados["genero"],
            Quantidade_disponivel=livro_dados["Quantidade_disponivel"],
            Quantidade_paginas=livro_dados["Quantidade_paginas"],
             status=livro_dados["status"],
            Autor=autor.id_autor,     
            Editora=editora.id_editora
        )
        db.session.add(livro)
        db.session.commit()
        return livro.to_dict()
    
    def atualizar_livro(self, id, livro_dados):
        livro= Livros.query.get(id)
        if livro:
            livro.titulo= livro_dados.get("titulo", livro.titulo)
            livro.Genero= livro_dados.get("genero", livro.Genero)
            livro.status= livro_dados.get("status", livro.status)
            livro.Quantidade_disponivel= livro_dados.get("Quantidade_disponivel", livro.Quantidade_disponivel)
            livro.Quantidade_paginas= livro_dados.get("Quantidade_paginas", livro.Quantidade_paginas)

            autor_id= livro_dados.get("autor_id")
            editora_id= livro_dados.get("editora_id")

            if autor_id:
                autor= Autor.query.get(autor_id)
                if not autor:
                    autor= Autor(nome=autor_id)
                    db.session.add(autor)
                    db.session.commit()
                livro.autor_id= autor.id
            
            if editora_id:
                editora= Editora.query.get(editora_id)
                if not editora:
                    editora= Editora(nome=editora_id)
                    db.session.add(editora)
                    db.session.commit()
                livro.editora_id= editora.id
            
            db.session.commit()
            return livro.to_dict()
        return None
        
    def deletar_livro(self,id):
        livro=Livros.query.get(id)
        if livro:
            db.session.delete(livro)
            db.session.commit()
            return True
        return False


            

    