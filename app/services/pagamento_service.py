from repositories.pagamento_repository import PagamentoRepository
from repositories.multa_repository import MultaRepository

class PagamentoService:
    def __init__(self, pagamento_repository: PagamentoRepository, multa_repository: MultaRepository):
        self.pagamento_repository = pagamento_repository
        self.multa_repository = multa_repository
    
    def processar_pagamento(self, multa_id, cliente_id, valor, metodo):
        # Validações
        if valor <= 0:
            raise ValueError("Valor do pagamento deve ser positivo")
        
        if metodo not in ['PIX', 'Cartão', 'Dinheiro']:
            raise ValueError("Método de pagamento inválido")
        
        # Criar pagamento
        pagamento = self.pagamento_repository.criar_pagamento(
            multa_id, cliente_id, valor, metodo
        )
        
        # Confirmar e desbloquear cliente
        pagamento_confirmado = self.pagamento_repository.confirmar_pagamento_e_desbloquear(pagamento['id'])
        
        # Atualizar status da multa
        self.multa_repository.atualizar_status(multa_id, 'Paga')
        
        return pagamento_confirmado