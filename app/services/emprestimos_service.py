from repositories.emprestimos_repository import EmprestimoRepository
from repositories.clientes_repository import ClienteRepository

class EmprestimoService:
    def __init__(self, emprestimo_repository: EmprestimoRepository):
        self.emprestimo_repository= emprestimo_repository

    def obter_todos_emprestimos(self):
        return self.emprestimo_repository.listar_todos()
    
    def obter_por_id(self, id_emprestimo):
        return self.emprestimo_repository.buscar_id(id_emprestimo)
    
    def listar_por_cliente(self, cliente_id):
        return self.emprestimo_repository.listar_por_cliente(cliente_id)
    
    def lista_por_livro(self, livro_id):
        return self.emprestimo_repository.listar_por_livro(livro_id)
    
    def listar_emprestimos_ativos(self):
        return self.emprestimo_repository.listar_emprestimos_ativos()
    
    def listar_emprestimos_vencidos(self):
        return self.emprestimo_repository.listar_emprestimos_atrasados()
    
    def criar_emprestimo(self, dados_emprestimo):
        if not dados_emprestimo.get('data_emprestimo') or not dados_emprestimo.get('data_devolucao'):
            raise ValueError("é necessario estipular as datas de emprestimo e de devolução")
        return self.emprestimo_repository.adicionar_emprestimo(dados_emprestimo)
    
    def atualizar_emprestimo(self, id_emprestimo, dados_emprestimo):
        emprestimo= self.emprestimo_repository.buscar_id(id_emprestimo)
        if not emprestimo:
            raise ValueError("emprestimo não encontrado")
        return self.emprestimo_repository.atualizar_emprestimo(id_emprestimo,dados_emprestimo)
    
    def deletar_emprestimo(self, id_emprestimo):
        emprestimo= self.emprestimo_repository.buscar_id(id_emprestimo)
        if not emprestimo:
            raise ValueError("emprestimo não encontrado")
        return self.emprestimo_repository.deletar_emprestimo(id_emprestimo)
    
    def finalizar_emprestimo(self, id_emprestimo):
        emprestimo= self.emprestimo_repository.buscar_id(id_emprestimo)
        if not emprestimo:
            raise ValueError("emprestimo não encontrado")
        return self.emprestimo_repository.finalizar_emprestimo(id_emprestimo)
    
    def bloquear_cliente(self, id_cliente):
        cliente_repo= ClienteRepository()
        cliente= cliente_repo.buscar_id(id_cliente)
        if not cliente:
            raise ValueError("cliente não encontrado")
        return self.emprestimo_repository.bloquear_cliente_por_atraso(id_cliente)
    
    def desbloquear_cliente(self, id_cliente):
        cliente_repo= ClienteRepository()
        cliente= cliente_repo.buscar_id(id_cliente)
        if not cliente:
            raise ValueError("cliente não encontrado")
        return self.emprestimo_repository.desbloquear_cliente(id_cliente)