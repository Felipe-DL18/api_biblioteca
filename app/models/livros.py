from config.db_config import db

class Livros(db.Model):
    __tablename__= 'Livros'

    id_livro= db.Column(db.Integer, primary_key=True)
    titulo= db.Column(db.String(100), nullable=False)
    Editora= db.Column(db.Integer, db.ForeignKey('editora.id_editora'))
    Genero= db.Column(db.String(100), nullable=False)
    Autor= db.Column(db.Integer, db.ForeignKey('autor.id_autor'))
    status= db.Column(db.String(100), nullable=False)
    Quantidade_disponivel= db.Column(db.Integer, nullable=False)
    Quantidade_paginas= db.Column(db.Integer, nullable=False)


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