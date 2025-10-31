from config.db_config import db

class Cliente(db.Model):
    #nome da tabela no banco de dados
    __tablename__='clientes'

    id = db.Column(db.Integer, primary_key=True)#id do cliente
    nome= db.Column(db.String(100), nullable=False)#nome do cliente
    email = db.Column(db.String(100), unique=True, nullable=False)#email do cliente
    CPF= db.Column(db.String(11), unique=True, nullable=False)#CPF do cliente
    status= db.Column(db.String(20), nullable=False, default='Permitido')#status do cliente (Permitido ou Bloqueado)

    #converte o objeto Autor para dicionário (para JSON)
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