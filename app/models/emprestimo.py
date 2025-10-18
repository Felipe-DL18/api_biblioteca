from config.db_config import db

class Emprestimo(db.Model):
    __tablename__='emprestimo'

    id_emprestimo= db.Column(db.Integer, primary_key=True)
    livro_id=db.Column(db.Integer, db.ForeignKey('Livros.id_livro'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    data_emprestimo=db.Column(db.Date, nullable=False)
    data_devolucao=db.Column(db.Date, nullable=False)
    data_devolvido=db.Column(db.Date, nullable=True)
    cliente = db.relationship('Cliente', backref='emprestimos')

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