from repositories.multa_repository import MultaRepository

class MultaService:
    def __init__(self, multa_repository: MultaRepository):
        self.multa_repository = multa_repository
    
    def obter_multas_cliente(self, cliente_id):
        if not cliente_id or cliente_id <= 0:
            raise ValueError("ID do cliente inválido")
        return self.multa_repository.buscar_por_cliente(cliente_id)
    
    def calcular_multa(self, dias_atraso):
        if dias_atraso <= 0:
            return 0.0
        return dias_atraso * 2.00  # R$ 2,00 por dia
    
    def criar_multa_automatica(self, emprestimo, dias_atraso):
        if dias_atraso > 0:
            valor_multa = self.calcular_multa(dias_atraso)
            return self.multa_repository.criar_multa(
                emprestimo_id=emprestimo.id_emprestimo,
                cliente_id=emprestimo.cliente_id,
                dias_atraso=dias_atraso,
                valor_total=valor_multa
            )
        return None