from config.db_config import db

class Cliente(db.Model):
    __tablename__='clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome= db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    CPF= db.Column(db.String(11), unique=True, nullable=False)
    status= db.Column(db.String(20), nullable=False, default='Permitido')

    def to_dict(self):
        data={
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cpf": self.CPF,
            "status": self.status,
            "emprestimos": [e.id_emprestimo for e in self.emprestimos]
        }
        return data