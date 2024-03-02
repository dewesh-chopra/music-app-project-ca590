from flask import Flask, flash, render_template, request, redirect, session, url_for

from encryption import encryption
from myemail import Email
from user import UserOperation
from validate import myvalidate
from myrandom import randomnum

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

objuser = UserOperation()

objvalid = myvalidate()

objemail = Email(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/user_signup", methods=["GET", "POST"])
def user_signup():
    if request.method == "GET":
        return render_template("user_signup.html")
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        uname = request.form['uname']
        password = request.form['password']

        # For validation
        myform = [fname, lname, email, uname, password]
        if not objvalid.required(myform):
            flash("Field cannot be left blank.")
            return redirect(url_for('user_signup'))

        # For encryption
        enc = encryption()
        password = enc.convert(password)

        # Check if already exists, then send to db
        userobj = UserOperation()
        bEmail = userobj.user_check_email(email)
        bUname = userobj.user_check_uname(uname)

        if not bEmail and not bUname:
            # Mailing module
            global otp
            otp = randomnum()
            subject="Music App's Email verification!"
            message = "Hi " + fname + ". Welcome to Music App. Your OTP is " + str(otp)
            objemail.compose_mail(subject, message, email=email)
            
            userobj.user_insert(fname, lname, email, uname, password)
            flash("OTP was sent to your given email ID.")
            return redirect(url_for('otpverify', email=email))
        elif not bEmail:
            flash("This email ID already exists.")
            return redirect(url_for('user_signup'))
        elif not bUname:
            flash("This username already exists.")
            return redirect(url_for('user_signup'))
        else:
            flash("User already exists Please change the username and email ID.")
            return redirect(url_for('user_signup'))

@app.route('/otpverify',methods=['GET','POST'])
def otpverify():
    if('otp' in globals()):
        if(request.method=='GET'):
            email = request.args.get('email')
            return render_template('otp.html',email=email)
        else:
            n1=request.form['n1']
            n2=request.form['n2']
            n3=request.form['n3']
            n4=request.form['n4']
            otpinput = n1+n2+n3+n4
            if(str(otpinput) == otpinput):
                flash("Successfully Registered...login now")
                return redirect(url_for('user_login'))
            else:
                email=request.form['email']
                objuser.user_delete(email)
                flash("Email Verification Failed... Register Again!!")
                return redirect(url_for('user_signup'))
    else:
        return "can't access this page" 

@app.route("/user_login", methods=['get', 'post'])
def user_login():
    if request.method == "GET":
        return render_template("user_login.html")
    else:
        uname = request.form['uname']
        password = request.form['password']

        enc = encryption()
        password = enc.convert(password)

        r = objuser.user_login(uname, password)
        if r == 0:
            flash("Invalid username and password!")
            return redirect(url_for('user_login'))
        else:
            return "Welcome " + session['uname']

if __name__ == "__main__":
    app.run(debug=True, port=5001)
