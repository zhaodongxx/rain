from email.mime.text import MIMEText
from email import encoders
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

import smtplib


class iEmail:
    def sendEmail(params, msg):
        print(params)

        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))

        msg = MIMEText(msg, 'plain', 'utf-8')

        # 输入Email地址和口令:
        from_addr = '694463348@qq.com'
        password = 'uyxbftyjtskfbbjc'  # 授权码
        # 输入收件人地址:
        to_addr = 'zhaodongxx@outlook.com'
        # 输入SMTP服务器地址:
        smtp_server = 'smtp.qq.com'

        msg['From'] = _format_addr('小雨 <%s>' % from_addr)
        msg['To'] = _format_addr('master <%s>' % to_addr)
        msg['Subject'] = Header('来自小雨的提醒邮件', 'utf-8').encode()

        import smtplib
        server = smtplib.SMTP_SSL(smtp_server, 465)  # SMTP协议默认端口是25
        #server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
