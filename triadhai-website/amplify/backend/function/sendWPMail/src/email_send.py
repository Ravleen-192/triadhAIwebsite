import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email_send_config import *
def compose_msg(to_address, name, surl):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Whitepaper from Triadh digital'
    msg['From'] = "Triadh AI <"+FROM_ADDR+">"
    msg['To'] = ', '.join([to_address])
    #msg['Cc'] = ', '.join(CC_ADDR)
    #msg['Bcc'] = ', '.join(BCC_ADDR)
    greeting = "Hi "+ name.upper() +",\n\n"
    regards = "Regards,\n Triadh Digital."
    linktxt = "Please click below to access your eBook.:\n\n"+surl+",\n"

    text = greeting + """
            Thank you for your interest in The Data Mesh ebook.\n
            """ + linktxt + regards
    BODY_HTML = """<div><table class="mktoModule desktopPad" id="spacerModule4cc6d2fb-f84c-47b5-80c0-de2839b7bda3" width="100%" height="35" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody>

                    <tr></tr> 

                    <td class="centerImage" align="center" style="padding-left:40px; padding-right:40px; padding-top:25px; padding-bottom:25px; background-color:#ffffff;"> 
                    <div class="mktoText" > 
                    <a href="https://www.triadh.digital" alt="Triadh Digital" title="Triadh Digital"> <img align="center" src="data:image/png;base64,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" alt="TriadhDigital" border="0" width="180" height="50" style="display:block; color:#0D9F98;"> </a> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule desktopPad" id="spacerModule4cc6d2fb-f84c-47b5-80c0-de2839b7bda3" width="100%" height="35" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="desktopPad" height="35" style="background-color:#ffffff; line-height:35px;font-size:35px;">&nbsp;</td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="h3833bc7b1-08bf-4a4d-b3c2-6525053cf030" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="color: #1b3139;	font-family:	Arial, Helvetica, sans-serif; font-size: 28px;line-height: 36px;background-color:#ffffff; padding-left:40px; padding-right:40px;"> 
                    <div class="mktoText" id="titlePlaceholder833bc7b1-08bf-4a4d-b3c2-6525053cf030"> 
                    <div style="text-align: center;"> 
                    <span style="font-size: 24px;">Thank you for your interest in The Helios Data Mesh ebook.</span> 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule desktopPad" id="spacerModule4cc6d2fb-f84c-47b5-80c0-de2839b7bda3dd485eea-d7be-4d48-9262-1bff755cdf8e" width="100%" height="35" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="desktopPad" height="35" style="background-color:#ffffff; line-height:35px;font-size:35px;">&nbsp;</td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="mainCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19f" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="font-family: Arial, Helvetica, sans-serif; font-size:13px; line-height:20px; color:#0D9F98; padding-left:40px; padding-right:40px;background-color:#ffffff;"> 
                    <div class="mktoText" id="mainCopyCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19f"> 
                    <div style="text-align: center;">
                    Please click below to access your eBook. 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule desktopPad" id="spacerModule4cc6d2fb-f84c-47b5-80c0-de2839b7bda38d03b63f-434f-429a-9bce-d3b6b9d1fe5c" width="100%" height="35" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="desktopPad" height="35" style="background-color:#ffffff; line-height:35px;font-size:35px;">&nbsp;</td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="oneButtonCTAc039e444-7d98-4d11-ad75-f3af53bdf869" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" align="center" style="background-color:#ffffff; padding-left:40px; padding-right:40px;"> 
                    <table align="center" class="" border="0" cellspacing="0" cellpadding="0" bgcolor= "#0D9F98" width="205" style="border-radius:5px;"> 
                    <tbody> 
                    <tr> 
                    <td style="font-family: Arial, Helvetica, sans-serif;	font-size: 18px;	line-height: 20px;	text-align: center; padding-top:15px; padding-right:26px; padding-bottom:15px; padding-left:26px;color:#ffffff;"> 
                    <div class="mktoText" > 
                    <a href=\"""" + surl + """\" title="" style="color: #ffffff; text-decoration: none;">Download Now</a> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="persistentSpacerModuleff32aa99-e394-477a-a8e3-3432f8496733" width="100%" height="35" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td height="35" style="background-color:#ffffff; line-height:35px;font-size:35px;">&nbsp;</td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="ctatext22d78cf9-8ead-45a4-9c5b-f605d6226cd7" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" bgcolor="#ffffff" align="center" style="padding-left:40px; padding-right:40px;background-color:#ffffff;font-size:20px; line-height:24px; color:#0D9F98;font-family:Arial, Helvetica, sans-serif;"> 
                    <div class="mktoText" id="linktext5d98b0fb-0ec8-49e4-ae59-8bf2f0792178"> 
                    <div style="font-family: Arial, Helvetica, Calibri, sans-serif; font-size: 20px; letter-spacing: none; line-height: 1.4; text-align: center; color: #000000;"> 

                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                        <table class="mktoModule" id="mainCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19f" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="font-family: Arial, Helvetica, sans-serif; font-size:13px; line-height:20px; color:#0D9F98; padding-left:40px; padding-right:40px;background-color:#ffffff;"> 
                    <div class="mktoText" id="mainCopyCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19f"> 
                    <div style="text-align: center;">
                    The Link will expire in one week. 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="mainCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19fdf651b2c-b4bf-4752-a90e-516f47cfef72" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="font-family: Arial, Helvetica, sans-serif; font-size:13px; line-height:20px; color:#1b3139; padding-left:40px; padding-right:40px;background-color:#ffffff;"> 
                    <div class="mktoText" id="mainCopyCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19fdf651b2c-b4bf-4752-a90e-516f47cfef72"> 
                    <div style="text-align: center;">
                    Let's keep the conversation going. 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    </div>
                    """

    print(text)
    # Record the MIME types of both parts - text/plain and text/html.
    bodytxt = MIMEText(text, 'plain')
    bodyhtm = MIMEText(BODY_HTML, 'html')

    # Attach parts into message container.
    msg.attach(bodytxt)
    msg.attach(bodyhtm)
    return msg

def ceo_compose_msg(to_address,name,title, company,phone,surl):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Whitepaper from Triadh digital'
    msg['From'] = "Triadh AI <"+FROM_ADDR+">"
    msg['To'] = ', '.join(BCC_ADDR)
    #msg['Cc'] = ', '.join(CC_ADDR)
    #greeting = "Hi "+ name.upper() +",\n\n"
    name_details = "Name:"+name.upper()+"\n\n"
    company_details = """\n\n""" + "Company: "+company.upper()
    job_details =  """\n\n""" +"Job Title: "+title.upper()  
    phone_details =  """\n\n""" + "Phone Number: "+phone+ """\n\n""" 
    regards = "Regards,\n Triadh Digital."
    linktxt = "Please click below to access your eBook.:\n\n"+surl+",\n"

    text = name_details + """\n\n""" + company_details + """\n\n""" + job_details + """\n\n""" + phone_details + """\n\n""" +"""
            Thank you for your interest in The Data Mesh ebook.\n
            """ + linktxt + regards
            
    BODY_HTML = """<div>              
                    <table class="mktoModule desktopPad" id="spacerModule4cc6d2fb-f84c-47b5-80c0-de2839b7bda3" width="100%" height="35" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody>
                    <tr>
                    <td class="centerImage" align="center" style="padding-left:40px; padding-right:40px; padding-top:25px; padding-bottom:25px; background-color:#ffffff;"> 
                    <div class="mktoText" > 
                    <a href="https://www.triadh.digital" alt="Triadh Digital" title="Triadh Digital"> <img align="center" src="data:image/png;base64,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" alt="TriadhDigital" border="0" width="180" height="50" style="display:block; color:#0D9F98;"> </a> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="h3833bc7b1-08bf-4a4d-b3c2-6525053cf030" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="color: #1b3139;	font-family:	Arial, Helvetica, sans-serif; font-size: 13px;line-height: 20px;background-color:#ffffff; padding-left:40px; padding-right:40px;"> 
                    <div class="mktoText" id="titlePlaceholder833bc7b1-08bf-4a4d-b3c2-6525053cf030"> 
                    <div style="text-align: center;"> 
                    <span style="font-size: 13px;">"""+ """\n\n""" + name_details + """\n\n""" + """</span> 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="mainCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19fdf651b2c-b4bf-4752-a90e-516f47cfef72" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="font-family: Arial, Helvetica, sans-serif; font-size:13px; line-height:20px; color:#1b3139; padding-left:40px; padding-right:40px;background-color:#ffffff;"> 
                    <div class="mktoText" id="mainCopyCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19fdf651b2c-b4bf-4752-a90e-516f47cfef72"> 
                    <div style="text-align: center;">
                    <span style="font-size: 13px;">"""+ """\n\n""" + company_details + """\n\n""" + """</span> 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="mainCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19fdf651b2c-b4bf-4752-a90e-516f47cfef72" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="font-family: Arial, Helvetica, sans-serif; font-size:13px; line-height:20px; color:#1b3139; padding-left:40px; padding-right:40px;background-color:#ffffff;"> 
                    <div class="mktoText" id="mainCopyCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19fdf651b2c-b4bf-4752-a90e-516f47cfef72"> 
                    <div style="text-align: center;">
                    <span style="font-size: 13px;">"""+ """\n\n""" + job_details + """\n\n""" + """</span> 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="mainCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19fdf651b2c-b4bf-4752-a90e-516f47cfef72" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="font-family: Arial, Helvetica, sans-serif; font-size:13px; line-height:20px; color:#1b3139; padding-left:40px; padding-right:40px;background-color:#ffffff;"> 
                    <div class="mktoText" id="mainCopyCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19fdf651b2c-b4bf-4752-a90e-516f47cfef72"> 
                    <div style="text-align: center;">
                    <span style="font-size: 13px;">"""+ """\n\n""" + phone_details + """\n\n""" + """</span> 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="h3833bc7b1-08bf-4a4d-b3c2-6525053cf030" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="color: #1b3139;	font-family:	Arial, Helvetica, sans-serif; font-size: 28px;line-height: 36px;background-color:#ffffff; padding-left:40px; padding-right:40px;"> 
                    <div class="mktoText" id="titlePlaceholder833bc7b1-08bf-4a4d-b3c2-6525053cf030"> 
                    <div style="text-align: center;"> 
                    <span style="font-size: 24px;">Thank you for your interest in The Helios Data Mesh ebook.</span> 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule desktopPad" id="spacerModule4cc6d2fb-f84c-47b5-80c0-de2839b7bda3dd485eea-d7be-4d48-9262-1bff755cdf8e" width="100%" height="35" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="desktopPad" height="35" style="background-color:#ffffff; line-height:35px;font-size:35px;">&nbsp;</td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="mainCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19f" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="font-family: Arial, Helvetica, sans-serif; font-size:13px; line-height:20px; color:#0D9F98; padding-left:40px; padding-right:40px;background-color:#ffffff;"> 
                    <div class="mktoText" id="mainCopyCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19f"> 
                    <div style="text-align: center;">
                    Please click below to access your eBook. 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule desktopPad" id="spacerModule4cc6d2fb-f84c-47b5-80c0-de2839b7bda38d03b63f-434f-429a-9bce-d3b6b9d1fe5c" width="100%" height="35" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="desktopPad" height="35" style="background-color:#ffffff; line-height:35px;font-size:35px;">&nbsp;</td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="oneButtonCTAc039e444-7d98-4d11-ad75-f3af53bdf869" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" align="center" style="background-color:#ffffff; padding-left:40px; padding-right:40px;"> 
                    <table align="center" class="" border="0" cellspacing="0" cellpadding="0" bgcolor= "#0D9F98" width="205" style="border-radius:5px;"> 
                    <tbody> 
                    <tr> 
                    <td style="font-family: Arial, Helvetica, sans-serif;	font-size: 18px;	line-height: 20px;	text-align: center; padding-top:15px; padding-right:26px; padding-bottom:15px; padding-left:26px;color:#ffffff;"> 
                    <div class="mktoText" > 
                    <a href=\"""" + surl + """\" title="" style="color: #ffffff; text-decoration: none;">Download Now</a> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="persistentSpacerModuleff32aa99-e394-477a-a8e3-3432f8496733" width="100%" height="35" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td height="35" style="background-color:#ffffff; line-height:35px;font-size:35px;">&nbsp;</td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="ctatext22d78cf9-8ead-45a4-9c5b-f605d6226cd7" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" bgcolor="#ffffff" align="center" style="padding-left:40px; padding-right:40px;background-color:#ffffff;font-size:20px; line-height:24px; color:#0D9F98;font-family:Arial, Helvetica, sans-serif;"> 
                    <div class="mktoText" id="linktext5d98b0fb-0ec8-49e4-ae59-8bf2f0792178"> 
                    <div style="font-family: Arial, Helvetica, Calibri, sans-serif; font-size: 20px; letter-spacing: none; line-height: 1.4; text-align: center; color: #000000;"> 

                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                        <table class="mktoModule" id="mainCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19f" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="font-family: Arial, Helvetica, sans-serif; font-size:13px; line-height:20px; color:#0D9F98; padding-left:40px; padding-right:40px;background-color:#ffffff;"> 
                    <div class="mktoText" id="mainCopyCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19f"> 
                    <div style="text-align: center;">
                    The Link will expire in one week. 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    <table class="mktoModule" id="mainCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19fdf651b2c-b4bf-4752-a90e-516f47cfef72" width="100%" border="0" cellpadding="0" cellspacing="0" style="min-width:100%;"> 
                    <tbody> 
                    <tr> 
                    <td class="stack" style="font-family: Arial, Helvetica, sans-serif; font-size:13px; line-height:20px; color:#1b3139; padding-left:40px; padding-right:40px;background-color:#ffffff;"> 
                    <div class="mktoText" id="mainCopyCopyc2d097f1-d84e-4c0a-bc5e-ce57c986a19fdf651b2c-b4bf-4752-a90e-516f47cfef72"> 
                    <div style="text-align: center;">
                    Let's keep the conversation going. 
                    </div> 
                    </div> </td> 
                    </tr> 
                    </tbody> 
                    </table>
                    </div>
                    """

    print(text)
    # Record the MIME types of both parts - text/plain and text/html.
    bodytxt = MIMEText(text, 'plain')
    bodyhtm = MIMEText(BODY_HTML, 'html')

    # Attach parts into message container.
    msg.attach(bodytxt)
    msg.attach(bodyhtm)
    return msg


class email_sender:
    def __init__(self):
        self.connection = None
        pass

    def connect(self):
        # Send the message via local SMTP server.
        self.connection = smtplib.SMTP(SMTP_SERVER, PORT_ADDRESS)
        print(self.connection,SMTP_SERVER)
        self.connection.set_debuglevel(1)
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.login(SMTP_USER, SMTP_PASSWORD)

    def disconnect(self):
        self.connection.quit()

    def send_email(self, to_address, msg, msg2):
        self.connection.sendmail(
            FROM_ADDR, [to_address] , msg.as_string())
       
        self.connection.sendmail(
            FROM_ADDR, [BCC_ADDR]  , msg2.as_string())
