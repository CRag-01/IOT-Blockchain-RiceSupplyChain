from twilio.rest import Client
account_sid = 'AC86da6cae659fd28ca8e22f2eca3fb25d'
auth_token = '4252735e53660594e84fd0dafd3755d4'
client = Client(account_sid, auth_token)

verification = client.verify \
                     .services('VAcfef5a1a850770131e72997309729345') \
                     .verifications \
                     .create(to='+919492909528', channel='sms')

print(verification.status)