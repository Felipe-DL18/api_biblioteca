from config.db_config import db

class Genero(db.Model):
    __tablename__="genero"

    id_genero=db.Column(db.Integer, primary_key=True)
    nome=db.Column(db.String(100), nullable=False)
    descricao=db.Column(db.String(100), nullable=False)
    livros= db.relationship('Livros', backref='genero', lazy=True)

    def to_dict(self):
        data={
            "id_genero":self.id_genero,
            "nome":self.nome,
            "descrição":self.descricao,
            "livros":[l.id_livro for l in self.livros]
        }
        return data