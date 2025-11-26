from models.funcionario import Funcionario
from config.db_config import db

class FuncionarioRepository:
    #buscar e mostrar todos os funcionarios
    def listar_funcionarios(self):
        funcionarios = Funcionario.query.all()
        return [f.to_dict() for f in funcionarios]
    
    #buscar e mostrar um funcionario via id
    def listar_por_id(self, id):
        funcionario = Funcionario.query.get(id)
        return funcionario.to_dict() if funcionario else None
    
    #adicionar um funcionario com os dados fornecidos 
    def adicionar_funcionario(self, dados_funcionario):
        novo_funcionario = Funcionario(
            nome=dados_funcionario["nome"],
            CPF=dados_funcionario["CPF"],
            email=dados_funcionario["email"],
            cargo_id=dados_funcionario["cargo_id"],
            salario=dados_funcionario["salario"]
        )

        # Adiciona o novo funcionario à sessão do banco
        db.session.add(novo_funcionario)
        #confirma a transação no banco de dados
        db.session.commit()
        #retorna o funcionario criado
        return novo_funcionario.to_dict()
    
    #atualiza um funcionario existente no banco
    def atualizar_funcionario(self, id, dados_funcionario):
        #busca esse funcionario pelo id
        funcionario= Funcionario.query.get(id)

        #se o id for encontrado atualiza os dados
        if funcionario:
            #atualiza os dados que foram fornecidos, caso contrário mantém o valor atual
            funcionario.nome = dados_funcionario.get("nome", funcionario.nome)
            funcionario.CPF = dados_funcionario.get("CPF", funcionario.CPF)
            funcionario.email = dados_funcionario.get("email", funcionario.email)
            funcionario.cargo_id = dados_funcionario.get("cargo_id", funcionario.cargo_id)
            funcionario.salario = dados_funcionario.get("salario", funcionario.salario)

            #comfirma as auterações no banco
            db.session.commit()
            #retorna o funcionario atualizado
            return funcionario.to_dict()

        #se o id não for encontrado retorna none
        return None
    
    #deleta um funcionario do banco
    def deletar_funcionario(self, id):
        #busca o funcionario pelo id
        funcionario = Funcionario.query.get(id)

        #se o funcionario for encontrado, deleta ele do banco
        if funcionario:
            #remove o funcionario da sessão do banco
            db.session.delete(funcionario)
            #confirma a transação no banco de dados
            db.session.commit()
            #retorna true
            return True
        
        #se o funcionario não for encontrado retorna false
        return False