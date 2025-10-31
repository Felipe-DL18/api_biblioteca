#importa as bibliotecas necessarias
from flask_mail import Message #importa a classe Message do flask_mail para criar e enviar emails
from config.db_config import db #importa a instancia do banco de dados
from models.emprestimo import Emprestimo #importa o modelo Emprestimo
from models.cliente import Cliente #importa o modelo Cliente
from models.livros import Livros #importa o modelo Livros
from datetime import datetime, timedelta #importa as classes datetime e timedelta do modulo datetime
import logging #importa a biblioteca logging para registrar logs de eventos

#define a classe NotificacaoService
class NotificacaoService:
    #construtor da classe
    def __init__(self, mail):
        self.mail=mail
        self.logger= logging.getLogger(__name__)

    #metodo para enviar email de vencimento
    def enviar_email_vencimento(self, cliente_email, cliente_nome, livro_titulo, data_devolucao):
        try:
            #configura o assunto e o corpo do email
            subject= "Emprestimo proximo do vencimento"
            #configura o corpo do email
            body=f"olá {cliente_nome}, o emprestimo do livro {livro_titulo} esta proximo da data de vencimento:{data_devolucao} "
            #cria a mensagem de email
            msg= Message(
                subject=subject,
                recipients=[cliente_email],
                body=body
            )

            #envia o email
            self.mail.send(msg)
            self.logger.info (f"Email enviado para {cliente_email} - Livro: {livro_titulo}") #registra um log de info sobre o email enviado
            #retorna True se o email for enviado com sucesso
            return True
        #trata excecoes durante o envio do email
        except Exception as e:
            self.logger.error(f"Erro ao enviar email para {cliente_email}: {str(e)}")
            return  False

    #metodo para verificar emprestimos perto de vencer   
    def verificar_emprestimo_perto_vencer(self):
        try:
            #calcula a data de vencimento (1 dia a partir de hoje)
            agora=datetime.now().date()
            vencer= agora+ timedelta(days=1)

            #consulta os emprestimos que ainda nao foram devolvidos e que vencem na data calculada
            emprestimos= Emprestimo.query.filter(
                Emprestimo.data_devolvido==None,
                Emprestimo.data_devolucao ==vencer
            ).all()
            #inicializa o contador de notificacoes
            notificacoes=0

            #envia notificacoes para cada emprestimo encontrado
            for emprestimo in emprestimos:
                #busca o cliente e o livro relacionados ao emprestimo
                cliente= Cliente.query.get(emprestimo.cliente_id)
                livro= Livros.query.get(emprestimo.livro_id)

                #verifica se o cliente e o livro existem
                if cliente and livro:
                    #envia o email de notificacao
                    sucesso = self.enviar_email_vencimento(
                        cliente_email=cliente.email,
                        cliente_nome=cliente.nome,
                        livro_titulo=livro.titulo,
                        data_devolucao=emprestimo.data_devolucao.strftime('%d/%m/%Y')
                    )
                    #incrementa o contador se o email foi enviado com sucesso
                    if sucesso:
                        notificacoes+=1

            #registra o numero de notificacoes enviadas      
            self.logger.info(f"Notificações enviadas: {notificacoes}")
            return notificacoes
            
        #trata excecoes durante a verificacao dos emprestimos
        except Exception as e:
            self.logger.error(f"Erro ao verificar empréstimos: {str(e)}")
            return 0