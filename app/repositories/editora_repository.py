from models.editora import Editora
from config.db_config import db

class EditoraRepository:
    #buscar e mostrar todas as editoras
    def listar_todas(self):
        editoras= Editora.query.all()
        return [editora.to_dict() for editora in editoras]
    
    #buscar e mostrar uma editora via id
    def buscar_por_id(self,id):
        editora= Editora.query.get(id)
        return editora.to_dict() if editora else None
    
    #adicionar uma editora com os dados fornecidos
    def adicionar_editora(self, dados_editora):
        editora=Editora(
            nome=dados_editora['nome'],
            pais=dados_editora['pais']
        )
        # Adiciona a nova editora à sessão do banco
        db.session.add(editora)
        #confirma a transação no banco de dados
        db.session.commit()
        #retorna a editora criada
        return editora.to_dict()
    
    #atualiza uma editora existente no banco
    def atualizar_editora(self, id, dados_editora):
        #busca essa editora pelo id
        editora= Editora.query.get(id)
        #se o id for encontrado atualiza os dados
        if editora:
            #atualiza o nome se for fornecido, caso contrário mantém o valor atual
            editora.nome= dados_editora.get('nome', editora.nome)
            #faz a mesma coisa com pais
            editora.pais= dados_editora.get('pais', editora.pais)
            #comfirma as auterações no banco
            db.session.commit()
            #retorna a editora atualizada
            return editora.to_dict()
        #se o id não for encontrado retorna none
        return None
    
    #deleta uma editora do banco
    def deletar_editora(self,id):
        #busca a editora pelo id
        editora= Editora.query.get(id)
        #se a editora for encontrada, deleta ela do banco
        if editora:
            #remove a editora da sessão do banco
            db.session.delete(editora)
            #confirma a transação no banco de dados
            db.session.commit()
            #retorna true
            return True
        #se a editora não for encontrada retorna false
        return False