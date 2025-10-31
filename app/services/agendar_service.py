from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from services.notificacao_service import NotificacaoService
import logging

class AgendarService:
    def __init__(self,mail, app):
        self.scheduler= BackgroundScheduler()
        self.notificacao_service= NotificacaoService(mail)
        self.app=app
        self.logger= logging.getLogger(__name__)

    def iniciar_agendamentos(self):
        try:
            #verificaacada 30 segundps
            self.scheduler.add_job(
                self.verificar_notificacoes,
                trigger= IntervalTrigger(seconds=30),
                id='verificar_notificacoes',
                name=' verificar emprestimo proximo a vencer',
                replace_existing=True
            )
            self.scheduler.start()
            self.logger.info("deu certo")
        except Exception as ex:
            self.logger.info(f"um trem deu errao: {str(ex)}")

    def verificar_notificacoes(self):
        with self.app.app_context():
            self.logger.info("verificando emprestimos prestes a vencer")
            count= self.notificacao_service.verificar_emprestimo_perto_vencer()
            if count>0:
                self.logger.info(f"{count} notificações enviadas")

    def parar_agendamento(self):
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                self.logger.info("agendador parado")
            else:
                self.logger.info("não está rodando")
        except Exception as ex:
            self.logger.info(f"deu algum erro {(ex)}")