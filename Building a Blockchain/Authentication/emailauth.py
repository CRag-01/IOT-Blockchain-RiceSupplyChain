from flask import *  
from random import *  
from email_otp import *

app = Flask(__name__) 
app.secret_key = 'EmailAuthenticationByShivamYadav2021'
@app.route('/')  
def index():  
    return render_template("homepage.html")  

@app.route('/verify',methods = ["POST"])  
def verify():  
    rec_email = request.form["email"]
       
    current_otp = sendEmailVerificationRequest(receiver=rec_email) # this function sends otp to the receiver and also returns the same otp for our session storage
    session['current_otp'] = current_otp
    return render_template('verify.html')  

@app.route('/validate',methods=["POST"])   
def validate():  
    # Actual OTP which was sent to the receiver
    current_user_otp = session['current_otp']
    print("Current User OTP",current_user_otp)
    
    # OTP Entered by the User
    user_otp = request.form['otp'] 
    print("User OTP : ", user_otp)
     
    if int(current_user_otp) == int(user_otp):  
        return "<h3> Your email has been successfully verified! </h3>"  
    else:
        return "<h3> Oops! Email Verification Failure, OTP does not match. </h3>"   


if __name__ == '__main__':  
    app.run(debug = True)