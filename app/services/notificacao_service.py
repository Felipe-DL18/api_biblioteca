from flask_mail import Message
from config.db_config import db
from models.emprestimo import Emprestimo
from models.cliente import Cliente
from models.livros import Livros
from datetime import datetime, timedelta
import logging

class NotificacaoService:
    def __init__(self, mail):
        self.mail=mail
        self.logger= logging.getLogger(__name__)

    def enviar_email_vencimento(self, cliente_email, cliente_nome, livro_titulo, data_devolucao):
        #metodo para enviar email de vencimento
        try:
            subject= "Emprestimo proximo do vencimento"

            body=f"olá {cliente_nome}, o emprestimo do livro {livro_titulo} esta proximo da data de vencimento:{data_devolucao} "

            msg= Message(
                subject=subject,
                recipients=[cliente_email],
                body=body
            )

            self.mail.send(msg)
            self.logger.info (f"Email enviado para {cliente_email} - Livro: {livro_titulo}")

            return True
    
        except Exception as e:
            self.logger.error(f"Erro ao enviar email para {cliente_email}: {str(e)}")
            return  False
        
    def verificar_emprestimo_perto_vencer(self):
        #verifica os emprestimos que estão a 1 minuto de vencer
        try:
            agora=datetime.now().date()
            vencer= agora+ timedelta(days=1)

            emprestimos= Emprestimo.query.filter(
                Emprestimo.data_devolvido==None,
                Emprestimo.data_devolucao ==vencer
            ).all()

            notificacoes=0

            for emprestimo in emprestimos:
                cliente= Cliente.query.get(emprestimo.cliente_id)
                livro= Livros.query.get(emprestimo.livro_id)

                if cliente and livro:
                    sucesso = self.enviar_email_vencimento(
                        cliente_email=cliente.email,
                        cliente_nome=cliente.nome,
                        livro_titulo=livro.titulo,
                        data_devolucao=emprestimo.data_devolucao.strftime('%d/%m/%Y')
                    )
                    if sucesso:
                        notificacoes+=1
                    
            self.logger.info(f"Notificações enviadas: {notificacoes}")
            return notificacoes
            
        except Exception as e:
            self.logger.error(f"Erro ao verificar empréstimos: {str(e)}")
            return 0