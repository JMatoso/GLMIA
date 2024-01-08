import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from rich import print

class Mailer:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
        ports = [587, 465]
        for port in ports:
            try:
                self.server = smtplib.SMTP(host='smtp.gmail.com', port=port)
                self.server.ehlo()
                self.server.starttls()
                self.server.login(self.email, self.password)
                break
            except Exception as e:
                print(e)
                print("[red]Ocorreu um erro ao iniciar o servidor de email.[/red]")
        
    def send(self, to, subject, body):
        if self.server is None:
            print("[red]O servidor de email não está ativo.[/red]")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))
            text = msg.as_string()
            self.server.sendmail(self.email, to, text)
            print("Email para {} enviado com sucesso.".format(to))
        except Exception as e:
            print(e)
            print("[red]Ocorreu um erro ao enviar o email para {}.[/red]".format(to))
        finally:
            self.server.quit()
        
    def close(self):
        self.server.quit()