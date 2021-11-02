from twilio.rest import Client
account_sid = 'ACc5dd94fee2f4e95d327cfb1f5fce1fe3'
auth_token = 'fb082f68901e29d0eef119a88a12ddaf'
client = Client(account_sid, auth_token)

verification = client.verify \
                     .services('VA94971f9b80e6e8d3f1b20867196144a3') \
                     .verifications \
                     .create(to='+919903622684', channel='sms')

print(verification.status)