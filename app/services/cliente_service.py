from repositories.clientes_repository import ClienteRepository

class ClienteService:
    def __init__(self,cliente_repository: ClienteRepository):
        self.cliente_repository= cliente_repository

    def obter_todos_clientes(self):
        return self.cliente_repository.listar_todos()
    
    def obter_cliente_por_id(self, cliente_id):
        return self.cliente_repository.buscar_id(cliente_id)
    
    def criar_cliente(self, dados_cliete):
        if not dados_cliete.get('nome') or not dados_cliete.get('email') or not dados_cliete.get('CPF'):
            raise ValueError("nome, email e cpf são obirgatorios")
        
        return self.cliente_repository.adicionar_cliente(dados_cliete)
    
    def atualizar_cliente(self, cliente_id, dados_cliente):
        clinte= self.cliente_repository.buscar_id(cliente_id)
        if not clinte:
            return ("cliente não encontrado")
        
        return self.cliente_repository.atualizar_cliente(cliente_id,dados_cliente)
    
    def deletar_cliente(self, cliente_id):
        cliente= self.cliente_repository.buscar_id(cliente_id)
        if not cliente:
            raise ValueError("cliente não encontrado")
        
        return self.cliente_repository.deletar_cliente(cliente_id)