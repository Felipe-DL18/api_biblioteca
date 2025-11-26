from models.cargo import Cargo
from config.db_config import db

class CargoRepository:
    #buscar e mostrar todos os cargos
    def listar_cargos(self):
        cargos = Cargo.query.all()
        return [cargo.to_dict() for cargo in cargos]
    
    #buscar e mostrar um cargo via id
    def listar_por_id(self, id):
        cargo = Cargo.query.get(id)
        return cargo.to_dict() if cargo else None
    
    #adicionar um cargo com os dados fornecidos
    def adicionar_cargo(self, dados_cargo):
        novo_cargo = Cargo(
            cargo=dados_cargo["cargo"],
            descricao=dados_cargo["descricao"],
            carga_horaria_dia=dados_cargo["carga_horaria_dia"]
        )

        # Adiciona o novo cargo à sessão do banco
        db.session.add(novo_cargo)
        #confirma a transação no banco de dados
        db.session.commit()
        #retorna o cargo criado
        return novo_cargo.to_dict()
    
    #atualiza um cargo existente no banco
    def atualizar_cargo(self, id, dados_cargo):
        #busca esse cargo pelo id
        cargo = Cargo.query.get(id)

        #se o id for encontrado atualiza os dados
        if cargo:
            #atualiza os dado que foram fornecidos, caso contrário mantém o valor atual
            cargo.cargo = dados_cargo.get("cargo", cargo.cargo)
            cargo.descricao = dados_cargo.get("descricao", cargo.descricao)
            cargo.carga_horaria_dia = dados_cargo.get("carga_horaria_dia", cargo.carga_horaria_dia)

            #confirma as auterações no banco
            db.session.commit()
            #retorna o cargo criado
            return cargo.to_dict()

        #se o id não for encontrado retorna none
        return None
    

    #deleta um autor do banco
    def deletar_cargo(self, id):
        #busca o cargo pelo id
        cargo = Cargo.query.get(id)

        #se o cargp for encontrado, deleta ele do banco
        if cargo:
            #remove o cargo da sessão do banco
            db.session.delete(cargo)
            #confirma a transação no banco de dados
            db.session.commit()
            #retorna true
            return True

        #se o cargo não for encontrado retorna false    
        return False