from models.livros import Livros
from models.autor import Autor
from models.cliente import Cliente
from models.emprestimo import Emprestimo
from config.db_config import db
from datetime import datetime

class EmprestimoRepository:
    def listar_todos(self):
        emprestimos= Emprestimo.query.all()
        return [emprestimo.to_dict() for emprestimo in emprestimos]
    
    def buscar_id(self,id):
        emprestimo= Emprestimo.query.get(id)
        return emprestimo.to_dict() if emprestimo else None

    def adicionar_emprestimo(self, emprestimo_dados):
        livro_id=emprestimo_dados["livro_id"]
        cliente_id= emprestimo_dados["cliente_id"]
        
        livro= Livros.query.get(livro_id)
        if not livro:
            raise ValueError("livro não encontrado")
        
        if livro.Quantidade_disponivel <=0:
            raise ValueError("livro não disponivel")
        
        cliente= Cliente.query.get(cliente_id)
        if not cliente:
            raise ValueError("cliente não encontrado")
        
        if getattr(cliente, 'status', None) == 'bloqueado':
            raise ValueError("Cliente bloqueado")
        
        data_emprestimo = datetime.now().date()
        data_devolucao_str = emprestimo_dados["data_devolucao"]
        data_devolucao = datetime.strptime(data_devolucao_str, '%Y-%m-%d').date()

        novo_emprestimo= Emprestimo(
            livro_id= livro_id,
            cliente_id=cliente_id,
            data_emprestimo= data_emprestimo,
            data_devolucao= data_devolucao,
            data_devolvido=None,
        )

        livro.Quantidade_disponivel -=1

        db.session.add(novo_emprestimo)
        db.session.commit()
        return novo_emprestimo.to_dict()
    
    def atualizar_emprestimo(self, id, dados_emprestimo):
        emprestimo= Emprestimo.query.get(id)
        if not emprestimo:
            return None
        
        if 'data_devolvido' in dados_emprestimo and not emprestimo.data_devolvido:
            livro= Livros.query.get(emprestimo.livro_id)
            livro.Quantidade_disponivel+=1

            emprestimo.data_devolvido= dados_emprestimo['data_devolvido']

            self._verificar_atraso_e_bloquear(emprestimo)

        data_devolucao_str = dados_emprestimo["data_devolucao"]
        data_devolucao = datetime.strptime(data_devolucao_str, '%Y-%m-%d').date()
        if 'data_devolucao' in dados_emprestimo:
            emprestimo.data_devolucao= data_devolucao


        db.session.commit()
        return emprestimo.to_dict()

    def _verificar_atraso_e_bloquear(self,emprestimo):
        data_devolvido = emprestimo.data_devolvido
        data_devolucao = emprestimo.data_devolucao
        if isinstance(data_devolvido, datetime):
            data_devolvido = data_devolvido.date()
        
        if isinstance(data_devolucao, datetime):
            data_devolucao = data_devolucao.date()

        if data_devolvido > data_devolucao:
            cliente= Cliente.query.get(emprestimo.cliente_id)
            if cliente:
                cliente.status="bloqueado"
        
    def deletar_emprestimo(self,id):
        emprestimo= Emprestimo.query.get(id)
        if emprestimo:
            if not emprestimo.data_devolvido:
                livro= Livros.query.get(emprestimo.livro_id)
                livro.Quantidade_disponivel +=1
            db.session.delete(emprestimo)
            db.session.commit()
            return True
        return False

    def finalizar_emprestimo(self, id):
        emprestimo= Emprestimo.query.get(id)
        if not emprestimo:
            return None
        
        if emprestimo.data_devolvido:
            raise ValueError("emprestimo já finalizado")
        
        livro= Livros.query.get(emprestimo.livro_id)
        cliente= Cliente.query.get(emprestimo.cliente_id)

        livro.Quantidade_disponivel +=1

        emprestimo.data_devolvido= datetime.now()

        self._verificar_atraso_e_bloquear(emprestimo)
        db.session.commit()
        return emprestimo.to_dict()
    
    def bloquear_cliente_por_atraso(self, cliente_id):
        cliente= Cliente.query.get(cliente_id)
        if cliente:
            cliente.status="bloqueado"
            db.session.commit()
            return True
        return False
    
    def desbloquear_cliente(self,cliente_id):
        cliente= Cliente.query.get(cliente_id)
        if cliente:
            cliente.status="Permitido"
            db.session.commit()
            return True
        return False

    def listar_por_cliente(self, id):
        emprestimos= Emprestimo.query.filter_by(cliente_id=id).all()
        return [emprestimo.to_dict() for emprestimo in emprestimos]
    
    def listar_por_livro(self,id):
        emprestimos= Emprestimo.query.filter_by(livros_id=id).all()
        return [emprestimos.to_dict() for emprestimos in emprestimos]
    
    def listar_emprestimos_ativos(self):
        emprestimos = Emprestimo.query.filter_by(data_devolvido=None).all()
        return [emp.to_dict() for emp in emprestimos]
    
    def listar_emprestimos_atrasados(self):
        hoje= datetime.now().date()
        emprestimos= Emprestimo.query.filter(
            Emprestimo.data_devolucao <hoje,
            Emprestimo.data_devolvido==None
        ).all()
        return [emprestimo.to_dict() for emprestimo in emprestimos]