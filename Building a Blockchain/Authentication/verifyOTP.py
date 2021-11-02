from twilio.rest import Client
import json
account_sid = 'AC86da6cae659fd28ca8e22f2eca3fb25d'
auth_token = '4252735e53660594e84fd0dafd3755d4'
client = Client(account_sid, auth_token)

recv_code = input("Enter the OTP: ")
verification_check = client.verify \
                           .services('VAcfef5a1a850770131e72997309729345') \
                           .verification_checks \
                           .create(to='+917890032256', code = recv_code)

json_data = json.loads(verification_check)
print(json_data)
if json_data['status'] == 'approved':
    print("OTP verified")
else:
    print("OTP not verified")
