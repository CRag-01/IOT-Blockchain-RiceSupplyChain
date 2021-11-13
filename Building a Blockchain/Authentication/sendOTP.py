from twilio.rest import Client
account_sid = 'Enter account sid'
auth_token = 'Enter auth token'
client = Client(account_sid, auth_token)

verification = client.verify \
                     .services('Enter service id') \
                     .verifications \
                     .create(to='+917890032256', channel='sms')

print(verification.status)