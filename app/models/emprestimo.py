from config.db_config import db

class Emprestimo(db.Model):
    #nome da tabela no banco de dados
    __tablename__='emprestimo'

    id_emprestimo= db.Column(db.Integer, primary_key=True)#id do emprestimo
    livro_id=db.Column(db.Integer, db.ForeignKey('Livros.id_livro'))#id do liro(chave estrangeira)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))#id do cliente(chave estrangeira)
    data_emprestimo=db.Column(db.Date, nullable=False)#data do emprestimo
    data_devolucao=db.Column(db.Date, nullable=False)#data prevista para devolucao
    data_devolvido=db.Column(db.Date, nullable=True)#data em que o livro foi devolvido
    cliente = db.relationship('Cliente', backref='emprestimos')#relacionamento com a tabela cliente

    #converte o objeto Autor para dicionário (para JSON)
    def to_dict(self):
        data={
            "id":self.id_emprestimo,
            "livro":self.livro_id,
            "cliente":self.cliente_id,
            "data emprestimo":self.data_emprestimo,
            "data devolucao":self.data_devolucao,
            "data devolvido":self.data_devolvido
        }
        return data