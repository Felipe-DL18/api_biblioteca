from config.db_config import db

class Autor(db.Model):
    __tablename__="autor"

    id_autor= db.Column(db.Integer, primary_key=True)
    nome= db.Column(db.String(100), nullable=False)
    nacionalidade= db.Column(db.String(100), nullable=False)
    livros= db.relationship('Livros', backref='autor', lazy=True)

    def to_dict(self):
        data={
            "id":self.id_autor,
            "nome":self.nome,
            "nacionalidade":self.nacionalidade,
            "livros":[l.id_livro for l in self.livros]
        }
        return data