from twilio.rest import Client
account_sid = 'ACd10ed520e5effa5ba697ec1820f3464e'
auth_token = 'c1009ef43f880e10d2189f8dca9f0a51'
client = Client(account_sid, auth_token)

verification = client.verify \
                     .services('VA0c2a5a9367d0d7e90fc1e14597ab5f06') \
                     .verifications \
                     .create(to='+917890032256', channel='sms')
# verification = client.verify \
#                      .services('VA0c2a5a9367d0d7e90fc1e14597ab5f06') \
#                      .verifications \
#                      .create(to='ayansadhukhan28@gmail.com', channel='email')

print(verification.status)