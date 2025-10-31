from config.db_config import db

class Autor(db.Model):
    #nome da tabela no banco de dados
    __tablename__="autor"

    #colunas da tabela
    id_autor= db.Column(db.Integer, primary_key=True)#id do autor
    nome= db.Column(db.String(100), nullable=False)#nome do autor
    nacionalidade= db.Column(db.String(100), nullable=False)#nacionalidade do autor
    livros= db.relationship('Livros', backref='autor', lazy=True)#relacionamento com a tabela livros

    #converte o objeto Autor para dicionário (para JSON)
    def to_dict(self):
        data={
            "id":self.id_autor,
            "nome":self.nome,
            "nacionalidade":self.nacionalidade,
            "livros":[l.id_livro for l in self.livros]
        }
        return data