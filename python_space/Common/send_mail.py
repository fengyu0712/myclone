import os
import smtplib
from email.header import Header
from  email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Common.conf import Read_conf
from  Common.log import Logger
from Conf import Project_path

conf_path= Project_path.Conf_path + "mail.conf"
class Mail:
    def __init__(self):
        conf=Read_conf(conf_path)
        self.senter = conf.get_value("Email","senter")
        self.passwords = conf.get_value("Email","passwords")
        self.mail_host = conf.get_value("Email","mail_host")
        self.mail_post = conf.get_value("Email","mail_post")
        self.receiver = conf.get_value("Email","receiver")
        self.senter_name=conf.get_value("Email","senter_name")
        self.receiver_name = conf.get_value("Email", "receiver_name")

    def creat_mail(self,report_fail,subject):
        self.msg = MIMEMultipart()
        self.msg['From'] = Header(self.senter_name, 'utf-8')
        self.msg['To'] = Header(self.receiver_name, 'utf-8')
        self.msg['Subject'] = Header(subject, 'utf-8')#添加主题

        content_1=open(report_fail,'rb').read()
        try:
            att1 = MIMEText(content_1, 'base64', 'utf-8')   #添加附件
            att1.add_header('Content-Disposition', 'attachment', filename=os.path.basename(report_fail))
            self.msg.attach(MIMEText(content_1, 'html', 'utf-8'))  # 添加邮件正文
            self.msg.attach(att1)
        except Exception as e:
            Logger().error(e)
    def sent_mail(self):
        try:
            smtp=smtplib.SMTP_SSL(self.mail_host,self.mail_post)  # 构建smtp实例化
            # smtp.connect()  # 链接邮箱服务器
            smtp.login(self.senter, self.passwords)  # 登录邮箱
            smtp.sendmail(self.senter,self.receiver, self.msg.as_string())  # 发送邮件
            Logger().info("邮件发送成功!")
        except Exception as e:
            Logger().error(e)
        # finally:
        #     smtp.close()




subject = '这是邮件主题'

report_fail= Project_path.TestReport_path + "2018-06-13 13_49_38TestReport.html"

if __name__=='__main__':
    m=Mail()
    m.creat_mail(report_fail,subject)
    m.sent_mail()









