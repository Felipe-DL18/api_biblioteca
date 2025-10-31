from repositories.clientes_repository import ClienteRepository

# service para cliente
class ClienteService:
    # inicializa o repositorio de cliente
    def __init__(self,cliente_repository: ClienteRepository):
        self.cliente_repository= cliente_repository

    # obtém todos os clientes
    def obter_todos_clientes(self):
        return self.cliente_repository.listar_todos()
    
    # obtém cliente por id
    def obter_cliente_por_id(self, cliente_id):
        return self.cliente_repository.buscar_id(cliente_id)
    
    #cria cliente
    def criar_cliente(self, dados_cliete):
        # validação de dados obrigatórios
        if not dados_cliete.get('nome') or not dados_cliete.get('email') or not dados_cliete.get('CPF'):
            #se não tiver nome, email ou cpf, lança erro
            raise ValueError("nome, email e cpf são obirgatorios")
        # adiciona o cliente no repositório
        return self.cliente_repository.adicionar_cliente(dados_cliete)
    
    #atualiza cliente
    def atualizar_cliente(self, cliente_id, dados_cliente):
        # busca o cliente pelo id
        clinte= self.cliente_repository.buscar_id(cliente_id)
        # se não encontrar, retorna mensagem de erro
        if not clinte:
            return ("cliente não encontrado")
        # atualiza o cliente no repositório
        return self.cliente_repository.atualizar_cliente(cliente_id,dados_cliente)
    
    #deleta cliente
    def deletar_cliente(self, cliente_id):
        # busca o cliente pelo id
        cliente= self.cliente_repository.buscar_id(cliente_id)
        # se não encontrar, lança erro
        if not cliente:
            raise ValueError("cliente não encontrado")
        # deleta o cliente no repositório
        return self.cliente_repository.deletar_cliente(cliente_id)