import random
import smtplib

def generateOTP(otp_size = 6):
    final_otp = ''
    for i in range(otp_size):
        final_otp = final_otp + str(random.randint(0,9))
    return final_otp

def sendEmailVerificationRequest(sender="rice.supplychain.verify@gmail.com",receiver="", custom_text="Hello, Your OTP is "):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    google_app_password = "Maheraja"
    server.login(sender,google_app_password)
    cur_otp = generateOTP()
    msg = custom_text +  cur_otp
    server.sendmail(sender,receiver,msg)
    server.quit()
    return cur_otp