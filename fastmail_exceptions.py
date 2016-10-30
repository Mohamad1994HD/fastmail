
class TemplateLoadException(Exception):
    def __init__(self, message=''):
        super(TemplateLoadException, self).__init__(message)


import smtplib


class MailException(smtplib.SMTPException):
    def __init__(self, message=''):
        super(MailException, self).__init__(message)


class InvalidMailException(MailException):
    def __init__(self, message='Invalid Email'):
        super(InvalidMailException, self).__init__(message)

