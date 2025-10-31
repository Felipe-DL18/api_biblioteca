from config.db_config import db

class Editora(db.Model):
    #nome da tabela no banco de dados
    __tablename__='editora'

    id_editora=db.Column(db.Integer, primary_key=True)#id da editora
    nome=db.Column(db.String(100), nullable=False)#nome da editora
    pais=db.Column(db.String(100), nullable=False)#pais da editora
    livros=db.relationship('Livros', backref='editora', lazy=True)#relacionamento com a tabela livros

    #converte o objeto Autor para dicionário (para JSON)
    def to_dict(self):
        data={
            "id":self.id_editora,
            "nome":self.nome,
            "pais":self.pais,
            "livros":[l.id_livro for l in self.livros]
        }
        return data