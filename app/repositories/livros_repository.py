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
    
    #buscar livro por id
    def obter_por_id(self, id):
        livro= Livros.query.get(id)
        return livro.to_dict() if livro else None
    
    #adicionar livro com os dados fornecidos
    def adicionar_livro(self, livro_dados):
        #verifica se o autor e a editora existem, se não existir cria eles
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
        # Adiciona o novo livro à sessão do banco
        db.session.add(livro)
        #confirma a transação no banco de dados
        db.session.commit()
        #retorna o livro criado
        return livro.to_dict()
    
    #atualiza um livro existente no banco
    def atualizar_livro(self, id, livro_dados):
        #busca esse livro pelo id
        livro= Livros.query.get(id)
        #se o id for encontrado atualiza os dados
        if livro:
            #atualiza o titulo se for fornecido, caso contrário mantém o valor atual
            livro.titulo= livro_dados.get("titulo", livro.titulo)
            #faz a mesma coisa com genero, status, quantidade disponivel e quantidade de paginas
            livro.Genero= livro_dados.get("genero", livro.Genero)
            livro.status= livro_dados.get("status", livro.status)
            livro.Quantidade_disponivel= livro_dados.get("Quantidade_disponivel", livro.Quantidade_disponivel)
            livro.Quantidade_paginas= livro_dados.get("Quantidade_paginas", livro.Quantidade_paginas)
            #atualiza autor e editora se fornecido
            if 'autor_id' in livro_dados:
                livro.Autor = livro_dados['autor_id']
        
            if 'editora_id' in livro_dados: 
                livro.Editora = livro_dados['editora_id']
            
            #comfirma as auterações no banco
            db.session.commit()
            #retorna o livro atualizado
            return livro.to_dict()
        return None
        
    #deleta um livro do banco
    def deletar_livro(self,id):
        #busca o livro pelo id
        livro=Livros.query.get(id)
        #se o livro for encontrado, deleta ele do banco
        if livro:
            #remove o livro da sessão do banco
            db.session.delete(livro)
            #confirma a transação no banco de dados
            db.session.commit()
            #retorna true
            return True
        #se o livro não for encontrado retorna false
        return False


            

    