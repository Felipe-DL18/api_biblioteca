# models/multa.py
from config.db_config import db
from datetime import datetime

class Multa(db.Model):
    __tablename__ = 'multa'
    
    id_multa = db.Column(db.Integer, primary_key=True)
    emprestimo_id = db.Column(db.Integer, db.ForeignKey('emprestimo.id_emprestimo'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    valor_total = db.Column(db.Numeric(10,2), nullable=False)
    dias_atraso = db.Column(db.Integer, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='Pendente')  # Pendente, Paga
    
    # Relacionamentos
    emprestimo = db.relationship('Emprestimo', backref='multas')
    cliente = db.relationship('Cliente', backref='multas')
    
    def to_dict(self):
        return {
            "id": self.id_multa,
            "emprestimo_id": self.emprestimo_id,
            "cliente_id": self.cliente_id,
            "valor_total": float(self.valor_total),
            "dias_atraso": self.dias_atraso,
            "data_criacao": self.data_criacao.isoformat(),
            "status": self.status
        }