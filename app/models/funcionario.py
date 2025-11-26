from config.db_config import db

class Funcionario(db.Model):
    #nome da tabela no banco de dados
    __tablename__ = 'funicionarios'

    id_funcionario = db.Column(db.Integer, primary_key=True)#id do funcionario
    nome = db.Column(db.String(100), nullable=False)#nome do funcionario
    CPF = db.Column(db.String(11), unique=True, nullable=False)#CPF do funcionario
    email = db.Column(db.String(100), unique=True, nullable=False)#email do funcionario
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargos.id_cargo'))#id do cargo do funcionario
    cargo = db.relationship('Cargo', backref='funcionarios')#relacionamento com a tabela funcionario
    salario = db.Column(db.Float, nullable=True)#salario do funcionario

    #converte o objeto Funcionario para dicionário (para JSON)
    def to_dict(self):
        data= {
            "id": self.id_funcionario,
            "nome": self.nome,
            "CPF": self.CPF,
            "email": self.email,
            "cargo": self.cargo_id,
            "salario": self.salario
        }
        return data
