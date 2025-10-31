#importa as bibliotecas necessarias
from apscheduler.schedulers.background import BackgroundScheduler #importa o agendador em segundo plano, para não bloquear a aplicação principal
from apscheduler.triggers.interval import IntervalTrigger #importa o gatilho de intervalo, para definir a frequência dos agendamentos
from services.notificacao_service import NotificacaoService #importa o serviço de notificações
import logging #importa a biblioteca de logging para registrar eventos e erros

class AgendarService:
    #inicializa o serviço de agendamento com o serviço de notificações e a aplicação Flask
    def __init__(self,mail, app):
        self.scheduler= BackgroundScheduler() #cria uma instância do agendador em segundo plano
        self.notificacao_service= NotificacaoService(mail) #cria uma instância do serviço de notificações
        self.app=app #armazena a aplicação Flask
        self.logger= logging.getLogger(__name__) #configura o logger para registrar eventos e erros

    #inicia os agendamentos
    def iniciar_agendamentos(self):
        try:
            #adiciona um trabalho ao agendador para verificar notificações a cada 30 segundos
            self.scheduler.add_job(
                self.verificar_notificacoes, #função a ser executada
                trigger= IntervalTrigger(seconds=30), #define o intervalo de 30 segundos
                id='verificar_notificacoes', #identificador único do trabalho
                name=' verificar emprestimo proximo a vencer', #nome do trabalho
                replace_existing=True #substitui o trabalho existente com o mesmo ID, se houver
            )
            #faz com que o agendador inicie a execução dos trabalhos agendados
            self.scheduler.start()
            self.logger.info("deu certo") #registra uma mensagem de sucesso no logger
        # captura qualquer exceção que ocorra durante o processo de agendamento
        except Exception as ex:
            self.logger.info(f"um trem deu errao: {str(ex)}")

    # função para verificar notificações de empréstimos prestes a vencer
    def verificar_notificacoes(self):
        # executa o código dentro do contexto da aplicação Flask
        with self.app.app_context():
            # registra uma mensagem informando que a verificação está em andamento
            self.logger.info("verificando emprestimos prestes a vencer")
            # chama o serviço de notificações para verificar empréstimos prestes a vencer e obtém a contagem de notificações enviadas
            count= self.notificacao_service.verificar_emprestimo_perto_vencer()
            # se alguma notificação foi enviada, registra a contagem no logger
            if count>0:
                self.logger.info(f"{count} notificações enviadas")

    # função para parar o agendador
    def parar_agendamento(self):
        try:
            # verifica se o agendador está em execução
            if self.scheduler.running:
                #se estiver em execução, para o agendador
                self.scheduler.shutdown()
                self.logger.info("agendador parado")
            #se não estiver em execução, registra uma mensagem informando que não está rodando
            else:
                self.logger.info("não está rodando")
        # captura qualquer exceção que ocorra durante o processo de parada do agendador
        except Exception as ex:
            self.logger.info(f"deu algum erro {(ex)}")