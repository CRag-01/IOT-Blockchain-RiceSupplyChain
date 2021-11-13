from twilio.rest import Client

account_sid = 'Enter account sid'
auth_token = 'YOUR-AUTH-TOKEN-HERE'
client = Client(account_sid, auth_token)

def phone_authentication(phone_num):
    verification = client.verify \
                        .services('Enter service id') \
                        .verifications \
                        .create(to=phone_num, channel='sms')
    print(verification.status)
    message = verify_OTP(phone_num)
    return message

def verify_OTP(phone_num):
    client = Client(account_sid, auth_token)
    recv_code = input("Enter the OTP: ")
    verification_check = client.verify \
                            .services('Enter service id') \
                            .verification_checks \
                            .create(to=phone_num, code = recv_code)
    return verification_check.status

    