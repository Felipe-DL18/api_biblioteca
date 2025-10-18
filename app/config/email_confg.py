from flask_mail import Mail #gerencia envio de emails
import logging
import smtplib

mail= Mail()

def init_mail(app):
    logging.basicConfig(level=logging.DEBUG)
    smtplib.debuglevel = 1
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com' #define o servidor de email que vamos usar
    app.config['MAIL_PORT']= 587 #define a porta de comunicação, 587 é a padrao
    app.config['MAIL_USE_TLS']= True #serve para criptografar a comunicação
    app.config['MAIL_USERNAME']='felipediaslopes14@gmail.com'#email q vai enviar as mensagens
    app.config['MAIL_PASSWORD'] ='bgua aikv jxub qvdv' #senha desse trem ai
    app.config['MAIL_DEFAULT_SENDER']='felipediaslopes14@gmail.com' #quando enviar um email sem remetnete especificado usara esse

    mail.init_app(app)#conecta o mail ao app