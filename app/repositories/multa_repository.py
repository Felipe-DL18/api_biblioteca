# repositories/multa_repository.py
from models.multa import Multa
from config.db_config import db
from datetime import datetime

class MultaRepository:
    
    def criar_multa(self, emprestimo_id, cliente_id, dias_atraso, valor_total):
        nova_multa = Multa(
            emprestimo_id=emprestimo_id,
            cliente_id=cliente_id,
            dias_atraso=dias_atraso,
            valor_total=valor_total,
            status='Pendente'
        )
        db.session.add(nova_multa)
        db.session.commit()
        return nova_multa.to_dict()
    
    def buscar_por_cliente(self, cliente_id):
        multas = Multa.query.filter_by(cliente_id=cliente_id).all()
        return [multa.to_dict() for multa in multas]
    
    def buscar_por_id(self, multa_id):
        multa = Multa.query.get(multa_id)
        return multa.to_dict() if multa else None
    
    def atualizar_status(self, multa_id, novo_status):
        multa = Multa.query.get(multa_id)
        if multa:
            multa.status = novo_status
            db.session.commit()
            return multa.to_dict()
        return None