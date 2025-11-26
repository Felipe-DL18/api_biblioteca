# repositories/pagamento_repository.py
from models.pagamento import Pagamento
from config.db_config import db

class PagamentoRepository:
    
    def criar_pagamento(self, multa_id, cliente_id, valor_pago, metodo_pagamento):
        novo_pagamento = Pagamento(
            multa_id=multa_id,
            cliente_id=cliente_id,
            valor_pago=valor_pago,
            metodo_pagamento=metodo_pagamento,
            status='Processando'
        )
        db.session.add(novo_pagamento)
        db.session.commit()
        return novo_pagamento.to_dict()
    
    def confirmar_pagamento(self, pagamento_id):
        pagamento = Pagamento.query.get(pagamento_id)
        if pagamento:
            pagamento.status = 'Confirmado'
            db.session.commit()
            return pagamento.to_dict()
        return None
    
    def confirmar_pagamento_e_desbloquear(self, pagamento_id):
        pagamento = Pagamento.query.get(pagamento_id)
        if pagamento:
            pagamento.status = 'Confirmado'
            
            # Desbloquear cliente automaticamente
            from models.cliente import Cliente
            cliente = Cliente.query.get(pagamento.cliente_id)
            if cliente and cliente.status == 'bloqueado':
                cliente.status = 'Permitido'
            
            db.session.commit()
            return pagamento.to_dict()
        return None