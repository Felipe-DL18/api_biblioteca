from config.db_config import db

class Editora(db.Model):
    __tablename__='editora'

    id_editora=db.Column(db.Integer, primary_key=True)
    nome=db.Column(db.String(100), nullable=False)
    pais=db.Column(db.String(100), nullable=False)
    livros=db.relationship('Livros', backref='editora', lazy=True)

    def to_dict(self):
        data={
            "id":self.id_editora,
            "nome":self.nome,
            "pais":self.pais,
            "livros":[l.id_livro for l in self.livros]
        }
        return data