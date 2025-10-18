from models.cliente import Cliente
from config.db_config import db

class ClienteRepository:
    def listar_todos(self):
        cliente= Cliente.query.all()
        return [c.to_dict() for c in cliente]
    
    def buscar_id(sef,id):
        cliente= Cliente.query.get(id)
        return cliente.to_dict() if cliente else None
    
    def adicionar_cliente(self, dados_cliente):
        novo_cliente= Cliente(
            nome= dados_cliente["nome"],
            email= dados_cliente["email"],
            CPF= dados_cliente["CPF"]
        )
        db.session.add(novo_cliente)
        db.session.commit()
        return novo_cliente.to_dict()
    
    def atualizar_cliente(self, id, dados_cliente):
        cliente= Cliente.query.get(id)
        if cliente:
            cliente.nome= dados_cliente.get("nome", cliente.nome)
            cliente.email= dados_cliente.get("email", cliente.email)
            cliente.CPF= dados_cliente.get("CPF", cliente.CPF)
            db.session.commit()
            return cliente.to_dict()
        return None
    
    def deletar_cliente(self,id):
        cliente= Cliente.query.get(id)
        if cliente:
            db.session.delete(cliente)
            db.session.commit()
            return True 
        return False