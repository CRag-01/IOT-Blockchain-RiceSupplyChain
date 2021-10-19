from twilio.rest import Client

account_sid = 'AC86da6cae659fd28ca8e22f2eca3fb25d'
auth_token = 'YOUR-AUTH-TOKEN-HERE'
client = Client(account_sid, auth_token)

def phone_authentication(phone_num):
    verification = client.verify \
                        .services('VAcfef5a1a850770131e72997309729345') \
                        .verifications \
                        .create(to=phone_num, channel='sms')
    print(verification.status)
    message = verify_OTP(phone_num)
    return message

def verify_OTP(phone_num):
    client = Client(account_sid, auth_token)
    recv_code = input("Enter the OTP: ")
    verification_check = client.verify \
                            .services('VAcfef5a1a850770131e72997309729345') \
                            .verification_checks \
                            .create(to=phone_num, code = recv_code)
    return verification_check.status

    