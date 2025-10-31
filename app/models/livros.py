from config.db_config import db

class Livros(db.Model):
    #nome da tabela no banco de dados
    __tablename__= 'Livros'

    id_livro= db.Column(db.Integer, primary_key=True)#id do livro
    titulo= db.Column(db.String(100), nullable=False)#titulo do livro
    Editora= db.Column(db.Integer, db.ForeignKey('editora.id_editora'))#id da editora(chave estrangeira)
    Genero= db.Column(db.String(100), nullable=False)#genero do livro
    Autor= db.Column(db.Integer, db.ForeignKey('autor.id_autor'))#aid do autor(chave estrangeira)
    status= db.Column(db.String(100), nullable=False)#status do livro
    Quantidade_disponivel= db.Column(db.Integer, nullable=False)#quantidade disponivel do livro
    Quantidade_paginas= db.Column(db.Integer, nullable=False)#quantidade de paginas do livro

    #converte o objeto Autor para dicionário (para JSON)
    def to_dict(self):
        data={
            "id":self.id_livro,
            "titulo":self.titulo,
            "Editora":self.Editora,
            "Genero":self.Genero,
            "Autor":self.Autor,
            "status":self.status,
            "Quantidade disponivel":self.Quantidade_disponivel,
            "Quantidade de paginas": self.Quantidade_paginas
        }
        return data