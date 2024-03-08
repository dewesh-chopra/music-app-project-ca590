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
    if 'otp' in globals():
        if request.method=='GET':
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

@app.route("/user_login", methods=["GET", "POST"])
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
            # return "Welcome " + session['uname']
            return render_template('user_dashboard.html')

# Logout module
@app.route('/user_logout', methods=["GET", "POST"])
def user_logout():
    if 'uname' in session:
        if request.method=='GET':
            session.clear()
            return render_template("user_logout.html")
    else:
        flash("You cannot access this page..please login")
        return redirect(url_for("user_login"))
    
# Delete module
@app.route('/delete_user_account', methods=["GET", "POST"])
def delete_user_account():
    if 'uname' in session:
        if request.method=='GET':
            objuser.user_delete(session['uname'])
            session.clear()
            return redirect(url_for("user_login"))
    else:
        flash("You cannot access this page..please login")
        return redirect(url_for("user_login"))

# User dashboard
@app.route('/user_dashboard', methods=["GET", "POST"])
def user_dashboard():
    if 'uname' in session:
        if request.method == 'GET':
            return render_template('user_dashboard.html')
    else:
        flash('Login to continue!')
        return render_template('user_login.html')

# User profile
@app.route('/user_profile', methods=["GET", "POST"])
def user_profile():
    if 'uname' in session:
        if request.method == 'GET':
            record = objuser.user_profile()
            return render_template('user_profile.html', record=record)
        elif request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            password = request.form['password']
            objuser.user_update(fname, lname, password)
            return redirect(url_for('user_profile'))
    else:
        flash('Login to continue!')
        return redirect(url_for('user_login'))

@app.errorhandler(404)
def not_found(e):
    return "NOT FOUND"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
