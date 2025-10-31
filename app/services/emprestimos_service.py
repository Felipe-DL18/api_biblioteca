from repositories.emprestimos_repository import EmprestimoRepository
from repositories.clientes_repository import ClienteRepository

# service para gerenciar operações relacionadas a empréstimos
class EmprestimoService:
    # inicializa o serviço com o repositório de empréstimos
    def __init__(self, emprestimo_repository: EmprestimoRepository):
        self.emprestimo_repository= emprestimo_repository

    # obtém todos os empréstimos
    def obter_todos_emprestimos(self):
        return self.emprestimo_repository.listar_todos()
    
    # obtém um empréstimo por ID
    def obter_por_id(self, id_emprestimo):
        return self.emprestimo_repository.buscar_id(id_emprestimo)
    
    # obtém empréstimos por ID do cliente
    def listar_por_cliente(self, cliente_id):
        return self.emprestimo_repository.listar_por_cliente(cliente_id)
    
    # obtém empréstimos por ID do livro
    def lista_por_livro(self, livro_id):
        return self.emprestimo_repository.listar_por_livro(livro_id)
    
    # obtém empréstimos ativos
    def listar_emprestimos_ativos(self):
        return self.emprestimo_repository.listar_emprestimos_ativos()
    
    # obtém empréstimos vencidos
    def listar_emprestimos_vencidos(self):
        return self.emprestimo_repository.listar_emprestimos_atrasados()
    
    # cria um novo empréstimo
    def criar_emprestimo(self, dados_emprestimo):
        # validação básica dos dados do empréstimo
        if not dados_emprestimo.get('data_emprestimo') or not dados_emprestimo.get('data_devolucao'):
            #se não tiver data de emprestimo ou devolução, lança erro
            raise ValueError("é necessario estipular as datas de emprestimo e de devolução")
        # adiciona o empréstimo no repositório
        return self.emprestimo_repository.adicionar_emprestimo(dados_emprestimo)
    
    # atualiza um empréstimo existente
    def atualizar_emprestimo(self, id_emprestimo, dados_emprestimo):
        # busca o empréstimo pelo ID
        emprestimo= self.emprestimo_repository.buscar_id(id_emprestimo)
        # se não encontrar, lança erro
        if not emprestimo:
            raise ValueError("emprestimo não encontrado")
        # atualiza o empréstimo no repositório
        return self.emprestimo_repository.atualizar_emprestimo(id_emprestimo,dados_emprestimo)
    
    # deleta um empréstimo
    def deletar_emprestimo(self, id_emprestimo):
        # busca o empréstimo pelo ID
        emprestimo= self.emprestimo_repository.buscar_id(id_emprestimo)
        # se não encontrar, lança erro
        if not emprestimo:
            raise ValueError("emprestimo não encontrado")
        # deleta o empréstimo no repositório
        return self.emprestimo_repository.deletar_emprestimo(id_emprestimo)
    
    # finaliza um empréstimo
    def finalizar_emprestimo(self, id_emprestimo):
        # busca o empréstimo pelo ID
        emprestimo= self.emprestimo_repository.buscar_id(id_emprestimo)
        # se não encontrar, lança erro
        if not emprestimo:
            raise ValueError("emprestimo não encontrado")
        # finaliza o empréstimo no repositório
        return self.emprestimo_repository.finalizar_emprestimo(id_emprestimo)
    
    # bloqueia um cliente por atraso
    def bloquear_cliente(self, id_cliente):
        # verifica se o cliente existe
        cliente_repo= ClienteRepository()
        cliente= cliente_repo.buscar_id(id_cliente)
        #se não encontrar, lança erro
        if not cliente:
            raise ValueError("cliente não encontrado")
        # bloqueia o cliente no repositório
        return self.emprestimo_repository.bloquear_cliente_por_atraso(id_cliente)
    
    # desbloqueia um cliente
    def desbloquear_cliente(self, id_cliente):
        #verifica se o cliente existe
        cliente_repo= ClienteRepository()
        cliente= cliente_repo.buscar_id(id_cliente)
        #se não encontrar, lança erro
        if not cliente:
            raise ValueError("cliente não encontrado")
        # desbloqueia o cliente no repositório
        return self.emprestimo_repository.desbloquear_cliente(id_cliente)