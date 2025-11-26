from config.db_config import db

class Cargo(db.Model):
    #nome da tabela no banco de dados
    __tablename__ = 'cargos'

    id_cargo = db.Column(db.Integer, primary_key=True)#id do cargo
    cargo = db.Column(db.String(100), nullable=False)#cargo do cargo
    descricao = db.Column(db.String(250), nullable=False)#descrição do cargo
    carga_horaria_dia = db.Column(db.Integer, nullable=False)#carga horaria diaria do cargo


    #converte o objeto Autor para dicionário (para JSON)
    def to_dict(self):
        data = {
            "id": self.id_cargo,
            "cargo": self.cargo,
            "descricao": self.descricao,
            "carga_horaria_dia": self.carga_horaria_dia
        }
        return data