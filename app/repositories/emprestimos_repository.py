from models.livros import Livros
from models.autor import Autor
from models.cliente import Cliente
from models.emprestimo import Emprestimo
from config.db_config import db
from datetime import datetime

class EmprestimoRepository:
    #listar todos os emprestimos
    def listar_todos(self):
        emprestimos= Emprestimo.query.all()
        return [emprestimo.to_dict() for emprestimo in emprestimos]
    
    #buscar emprestimo por id
    def buscar_id(self,id):
        emprestimo= Emprestimo.query.get(id)
        return emprestimo.to_dict() if emprestimo else None

    # adicionar um emprestimo
    def adicionar_emprestimo(self, emprestimo_dados):
        livro_id=emprestimo_dados["livro_id"]
        cliente_id= emprestimo_dados["cliente_id"]
        
        #verificar se o livro existe e está disponivel
        livro= Livros.query.get(livro_id)
        #se não for encontrado retornas um erro
        if not livro:
            raise ValueError("livro não encontrado")
        
        #verificar se o livro está disponivel, se a quantidade for menor ou igual a 0, retorno um erro
        if livro.Quantidade_disponivel <=0:
            raise ValueError("livro não disponivel")
        
        #buscar o cliente pelo id
        cliente= Cliente.query.get(cliente_id)
        #se não encontrar retorna um erro
        if not cliente:
            raise ValueError("cliente não encontrado")
        
        #verificar se o cliente está bloqueado, se estiver retorna um erro
        if getattr(cliente, 'status', None) == 'bloqueado':
            raise ValueError("Cliente bloqueado")
        
        #data do emprestimo é a data atual
        data_emprestimo = datetime.now().date()
        #converter a data de devolução de string para objeto date
        data_devolucao_str = emprestimo_dados["data_devolucao"]
        #converter a string para objeto date
        data_devolucao = datetime.strptime(data_devolucao_str, '%Y-%m-%d').date()

        novo_emprestimo= Emprestimo(
            livro_id= livro_id,
            cliente_id=cliente_id,
            data_emprestimo= data_emprestimo,
            data_devolucao= data_devolucao,
            data_devolvido=None,
        )

        #diminuir a quantidade disponivel do livro em 1
        livro.Quantidade_disponivel -=1

        #adicionar o novo emprestimo ao banco
        db.session.add(novo_emprestimo)
        #confirma a transação no banco
        db.session.commit()
        #retorna o emprestimo criado
        return novo_emprestimo.to_dict()
    
    # atualizar um emprestimo
    def atualizar_emprestimo(self, id, dados_emprestimo):
        #buscar o emprestimo pelo id
        emprestimo= Emprestimo.query.get(id)
        #se não for encontrado retorna none
        if not emprestimo:
            return None
        
        #verifica se a data_devolvido está sendo atualizada
        if 'data_devolvido' in dados_emprestimo and not emprestimo.data_devolvido:
            #ajustar a quantidade disponivel do livro
            livro= Livros.query.get(emprestimo.livro_id)
            livro.Quantidade_disponivel+=1

            #atualiza a data_devolvido
            emprestimo.data_devolvido= dados_emprestimo['data_devolvido']

            #verifica se houve atraso na devolução
            self._verificar_atraso_e_bloquear(emprestimo)

        #converter a data_devolucao de string para date, se fornecida
        data_devolucao_str = dados_emprestimo["data_devolucao"]
        data_devolucao = datetime.strptime(data_devolucao_str, '%Y-%m-%d').date()
        #atualiza a data_devolucao se fornecida
        if 'data_devolucao' in dados_emprestimo:
            emprestimo.data_devolucao= data_devolucao

        #confirma as alterações no banco
        db.session.commit()
        #retorna o emprestimo atualizado
        return emprestimo.to_dict()

    #verifica se houve atraso na devolução e bloqueia o cliente se necessário
    # um cliente é bloqueado quando devolve o livro após a data prevista de devolução
    def _verificar_atraso_e_bloquear(self,emprestimo):
        #pega a data devolvido e data devolução
        data_devolvido = emprestimo.data_devolvido
        data_devolucao = emprestimo.data_devolucao
        #converte datetime para date se necessário
        if isinstance(data_devolvido, datetime):
            data_devolvido = data_devolvido.date()

        if isinstance(data_devolucao, datetime):
            data_devolucao = data_devolucao.date()

        #verifica se a data devolvido é maior que a data devolução
        if data_devolvido > data_devolucao:
            #busca o cliente e bloqueia ele
            cliente= Cliente.query.get(emprestimo.cliente_id)
            if cliente:
                cliente.status="bloqueado"
    
    # deletar um emprestimo
    def deletar_emprestimo(self,id):
        #buscar o emprestimo pelo id
        emprestimo= Emprestimo.query.get(id)
        #se for encontrado, deleta o emprestimo
        if emprestimo:
            #ajustar a quantidade disponivel do livro se o emprestimo não foi finalizado
            if not emprestimo.data_devolvido:
                livro= Livros.query.get(emprestimo.livro_id)
                livro.Quantidade_disponivel +=1
            #remove o emprestimo da sessão do banco
            db.session.delete(emprestimo)
            #confirma a transação no banco
            db.session.commit()
            #retorna true
            return True
        #se não for encontrado retorna false
        return False

    # finalizar um emprestimo
    def finalizar_emprestimo(self, id):
        #buscar o emprestimo pelo id
        emprestimo= Emprestimo.query.get(id)
        #se não for encontrado retorna none
        if not emprestimo:
            return None
        
        #verifica se o emprestimo já foi finalizado
        if emprestimo.data_devolvido:
            raise ValueError("emprestimo já finalizado")
        
        #ajustar a quantidade disponivel do livro
        livro= Livros.query.get(emprestimo.livro_id)
        cliente= Cliente.query.get(emprestimo.cliente_id)

        livro.Quantidade_disponivel +=1

        #definir a data_devolvido como a data atual
        emprestimo.data_devolvido= datetime.now()
        #verifica se houve atraso na devolução
        self._verificar_atraso_e_bloquear(emprestimo)
        #confirma as alterações no banco
        db.session.commit()
        #retorna o emprestimo finalizado
        return emprestimo.to_dict()
    
    # bloquear cliente por atraso
    def bloquear_cliente_por_atraso(self, cliente_id):
        #buscar o cliente pelo id
        cliente= Cliente.query.get(cliente_id)
        #se for encontrado, bloqueia o cliente
        if cliente:
            cliente.status="bloqueado"
            db.session.commit()
            return True
        #se não for encontrado retorna false
        return False
    
    #desbloquear cliente
    def desbloquear_cliente(self,cliente_id):
        #buscar o cliente pelo id
        cliente= Cliente.query.get(cliente_id)
        #se for encontrado, desbloqueia o cliente
        if cliente:
            cliente.status="Permitido"
            db.session.commit()
            return True
        #se não for encontrado retorna false
        return False

    # listar emprestimos pelo id do cliente
    def listar_por_cliente(self, id):
        emprestimos= Emprestimo.query.filter_by(cliente_id=id).all()
        return [emprestimo.to_dict() for emprestimo in emprestimos]
    
    # listar emprestimos pelo id do livro
    def listar_por_livro(self,id):
        emprestimos= Emprestimo.query.filter_by(livros_id=id).all()
        return [emprestimo.to_dict() for emprestimo in emprestimos]
    
    # listar emprestimos ativos (não devolvidos)
    def listar_emprestimos_ativos(self):
        emprestimos = Emprestimo.query.filter_by(data_devolvido=None).all()
        return [emp.to_dict() for emp in emprestimos]
    
    # listar emprestimos atrasados
    def listar_emprestimos_atrasados(self):
        #pega a data de hoje
        hoje= datetime.now().date()
        #filtra os emprestimos onde a data_devolucao é menor que hoje e data_devolvido é None
        emprestimos= Emprestimo.query.filter(
            Emprestimo.data_devolucao <hoje,
            Emprestimo.data_devolvido==None
        ).all()
        #retorna a lista de emprestimos atrasados
        return [emprestimo.to_dict() for emprestimo in emprestimos]