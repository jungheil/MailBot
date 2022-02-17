import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import markdown


class MailBot:
    def __init__(self, smtp_host, smtp_port, user, passwd):
        self.__smtp_host = smtp_host
        self.__smtp_port = smtp_port
        self.__smtp_user = user
        self.__smtp_pass = passwd
        self.__smtpObj = smtplib.SMTP_SSL()

    def Send(self, sender, receiver, subject, body, body_type='plain', attaches=[]):
        """_summary_

        Args:
            sender (_type_): sender email.
            receiver (_type_): receiver email.
            subject (_type_): subject.
            body (_type_): body content.
            body_type (str, optional): body content type. include 'plain', 'html', and 'md'. Defaults to 'plain'.
            attaches (list, optional): attaches to send. e.g. [(open('demo.jpg','rb),'att.jpg'),...]. Defaults to [].

        Returns:
            _type_: info. e.g. {'status': True,...}
        """        
        message = MIMEMultipart()
        if body_type == 'html':
            message.attach(MIMEText(body, 'html', 'utf-8'))
        elif body_type == 'md':
            body = self.__md2html(body)
            message.attach(MIMEText(body, 'html', 'utf-8'))
        else:
            message.attach(MIMEText(body, 'plain', 'utf-8'))

        message['From'] = Header(sender)
        message['To'] = Header(receiver)
        message['Subject'] = Header(subject, 'utf-8')
        if isinstance(attaches, list):
            for i in attaches:
                att = MIMEText(i[0], 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att["Content-Disposition"] = 'attachment; filename={}'.format(i[1])
                message.attach(att)
        else:
            att = MIMEText(attaches[0], 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename={}'.format(attaches[1])
            message.attach(att)
        try:
            self.__smtpObj = smtplib.SMTP_SSL(self.__smtp_host, self.__smtp_port)
            self.__smtpObj.login(self.__smtp_user, self.__smtp_pass)
            self.__smtpObj.sendmail(sender, receiver, message.as_string())
            print('MailBot Send Successful!')
            return {'status': True, 'body': body, 'subj': subject, 'sender': sender, 'receiver': receiver, 'type': body_type, 'attaches': ', '.join([i[1] for i in attaches])}
        except Exception as e:
            print(e)
            return {'status': False, 'body': body, 'subj': subject, 'sender': sender, 'receiver': receiver, 'type': body_type, 'attaches': ', '.join([i[1] for i in attaches]), 'error': str(e)}

    def __md2html(self, content):
        html_template = '''
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>email</title>
</head>
<body>
{}
</body>
</html>
'''
        return html_template.format(markdown.markdown(content))
