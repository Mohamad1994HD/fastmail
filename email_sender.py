import smtplib
import re

mail_regex = re.compile('[^@]+@[^@]+\.[^@]+')


class MailException(smtplib.SMTPException):
    def __init__(self, message=''):
        super(MailException, self).__init__(message)


class InvalidMailException(MailException):
    def __init__(self, message='Invalid Email'):
        super(InvalidMailException, self).__init__(message)


class Mail:

    def __init__(self, port=0, host='', usermail='', password='', tls=False):
        self.port = port
        self.host = host
        self.usermail = usermail
        self.password = password
        self.tls = tls

    def send(self, subject='', body='', to=''):
        if not self.check_mail(to):
            raise InvalidMailException(message='{0} is invalid mail address'.format(to))

        msg = """From: {0}\nTo: {1}\nSubject: {2}\n\n{3}""".format(self.usermail,
                                                                   to,
                                                                   subject,
                                                                   body)
        if self.tls:
            server = smtplib.SMTP(host=self.host, port=self.port)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(host=self.host, port=self.port)

        try:
            server.ehlo()
            server.login(user=self.usermail, password=self.password)
            server.sendmail(from_addr=self.usermail, to_addrs=to, msg=msg)
            server.close()
        except smtplib.SMTPException as e:
            raise MailException(message=str(e))

    def check_mail(self, mail):
        if re.match(mail_regex, mail):
            return True
        return False
