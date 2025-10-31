from models.cliente import Cliente
from config.db_config import db

class ClienteRepository:
    #buscar e mostrar todos os clientes
    def listar_todos(self):
        cliente= Cliente.query.all()
        return [c.to_dict() for c in cliente]
    
    #buscar e mostrar um cliente via id
    def buscar_id(sef,id):
        cliente= Cliente.query.get(id)
        return cliente.to_dict() if cliente else None
    
    #adicionar um cliente com os dados fornecidos
    def adicionar_cliente(self, dados_cliente):
        novo_cliente= Cliente(
            nome= dados_cliente["nome"],
            email= dados_cliente["email"],
            CPF= dados_cliente["CPF"]
        )
        #adiciona o novo cliente à sessão do banco
        db.session.add(novo_cliente)
        #confirma a transação no banco de dados
        db.session.commit()
        #retorna o cliente criado
        return novo_cliente.to_dict()
    
    #atualiza um cliente existente no banco
    def atualizar_cliente(self, id, dados_cliente):
        #busca esse cliente pelo id
        cliente= Cliente.query.get(id)
        #se o id for encontrado atualiza os dados
        if cliente:
            #atualiza o nome se for fornecido, caso contrário mantém o valor atual
            cliente.nome= dados_cliente.get("nome", cliente.nome)
            #faz a mesma coisa com email e CPF
            cliente.email= dados_cliente.get("email", cliente.email)
            #faz a mesma coisa com o cof
            cliente.CPF= dados_cliente.get("CPF", cliente.CPF)
            #comfirma as auterações no banco
            db.session.commit()
            #retorna o cliente atualizado
            return cliente.to_dict()
        #se o id não for encontrado retorna none
        return None
    
    #deleta um cliente do banco
    def deletar_cliente(self,id):
        #busca o cliente pelo id
        cliente= Cliente.query.get(id)
        #se o cliente for encontrado, deleta ele do banco
        if cliente:
            #remove o cliente da sessão do banco
            db.session.delete(cliente)
            #confirma a transação no banco de dados
            db.session.commit()
            #retorna true
            return True 
        #se o cliente não for encontrado retorna false
        return False