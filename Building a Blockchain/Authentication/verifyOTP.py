from twilio.rest import Client
import json
account_sid = 'Enter account sid'
auth_token = 'Enter auth token'
client = Client(account_sid, auth_token)

recv_code = input("Enter the OTP: ")
verification_check = client.verify \
                           .services('Enter service id') \
                           .verification_checks \
                           .create(to='+917890032256', code = recv_code)

# json_data = json.loads(verification_check)
# print(json_data)
if json_data['status'] == 'approved':
    print("OTP verified")
else:
    print("OTP not verified")
