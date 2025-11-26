# models/pagamento.py
from config.db_config import db
from datetime import datetime

class Pagamento(db.Model):
    __tablename__ = 'pagamento'
    
    id_pagamento = db.Column(db.Integer, primary_key=True)
    multa_id = db.Column(db.Integer, db.ForeignKey('multa.id_multa'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    valor_pago = db.Column(db.Numeric(10,2), nullable=False)
    data_pagamento = db.Column(db.DateTime, default=datetime.now)
    metodo_pagamento = db.Column(db.String(50))  # PIX, Cartão, Dinheiro
    status = db.Column(db.String(20), default='Processando')  # Processando, Confirmado
    
    # Relacionamentos
    multa = db.relationship('Multa', backref='pagamentos')
    cliente = db.relationship('Cliente', backref='pagamentos')
    
    def to_dict(self):
        return {
            "id": self.id_pagamento,
            "multa_id": self.multa_id,
            "cliente_id": self.cliente_id,
            "valor_pago": float(self.valor_pago),
            "data_pagamento": self.data_pagamento.isoformat(),
            "metodo_pagamento": self.metodo_pagamento,
            "status": self.status
        }