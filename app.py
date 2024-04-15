from flask import Flask, flash, render_template, request, redirect, session, url_for
from datetime import datetime

from encryption import encryption
from myemail import Email
from validate import myvalidate
from myrandom import randomnum
from audio import voice

from user import UserOperation
from creator import CreatorOperation


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

objuser = UserOperation()
objcreator = CreatorOperation()
objvalid = myvalidate()
objemail = Email(app)

@app.route("/")
def home():
    return render_template("index.html")

# USER MODULES

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

# Same used for creator module as well
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
            if session['uname']:    # USER
                if(str(otpinput) == otpinput):
                    flash("Successfully Registered...login now")
                    return redirect(url_for('user_login'))
                else:
                    email=request.form['email']
                    objuser.user_delete(email)
                    flash("Email Verification Failed... Register Again!!")
                    return redirect(url_for('user_signup'))
            if session['cname']:    # CREATOR
                if(str(otpinput) == otpinput):
                    flash("Successfully Registered...login now")
                    return redirect(url_for('creator_login'))
                else:
                    email=request.form['email']
                    objuser.creator_delete(email)
                    flash("Email Verification Failed... Register Again!!")
                    return redirect(url_for('creator_signup'))
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
            flash("You are logged out!")
            return redirect(url_for("user_login"))
    else:
        flash("You cannot access this page..please login")
        return redirect(url_for("user_login"))
    
# Edit password module
@app.route('/edit_password', methods=["GET", "POST"])
def edit_password():
    if 'uname' in session:
        if request.method=='GET':
            return render_template("edit_password.html")
        elif request.method=='POST':
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            # validate passwords
            data = [old_password, new_password]
            if not objvalid.required(data):
                flash("Please do not enter blank text as password!")
                return redirect(url_for("edit_password"))
            # Encrypt/decrypt
            enc = encryption()
            old_password = enc.convert(old_password)
            if objuser.match_password(session['uname'], old_password)==True:
                enc = encryption()
                new_password = enc.convert(new_password)
                objuser.change_password(session['uname'], new_password)
                flash('Password successfully changed.')
                return redirect(url_for("user_profile"))
            else:
                flash('Old password is incorrect.')
                return redirect(url_for("edit_password"))
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
            flash("Account deleted successfully!")
            return redirect(url_for("user_signup"))
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
            objuser.user_update(fname, lname)
            return redirect(url_for('user_profile'))
    else:
        flash('Login to continue!')
        return redirect(url_for('user_login'))

@app.route('/user_blog_listen',methods=['GET','POST'])
def user_blog_listen():
    if('uname' in session):
        if(request.method == 'GET'):
            record = objuser.user_blog_listen()
            return render_template("user_blog_listen.html", record=record)
    else:
        flash("you can't access this page..please login to continue")
        return redirect(url_for('user_login'))
    
@app.route('/user_song_listen',methods=['GET','POST'])
def user_song_listen():
    if('uname' in session):
        if(request.method == 'GET'):
            record = objuser.user_song_listen()
            return render_template("user_song_listen.html", record=record)
    else:
        flash("you can't access this page..please login to continue")
        return redirect(url_for('user_login'))


# CREATOR MODULES

@app.route("/creator_signup", methods=["GET", "POST"])
def creator_signup():
    if request.method == "GET":
        return render_template("creator_signup.html")
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cname = request.form['cname']
        password = request.form['password']
        photo = request.files['photo']

        # For validation
        myform = [fname, lname, email, cname, password]
        if not objvalid.required(myform):
            flash("Field cannot be left blank.")
            return redirect(url_for('creator_signup'))
        
        # For photo
        p = photo.filename
        if p=='':
            flash("Photo must be uploaded!")
            return redirect(url_for('creator_signup'))
        d = datetime.now()
        t = int(round(d.timestamp()))
        path = str(t) + '.' + p.split('.')[-1]
        photo.save('static/img/creator/' + path)

        # For encryption
        enc = encryption()
        password = enc.convert(password)

        # Check if already exists, then send to db
        bEmail = objcreator.creator_check_email(email)
        bCname = objcreator.creator_check_cname(cname)

        if not bEmail and not bCname:
            # Mailing creator
            global otp
            otp = randomnum()
            subject="Music App's Email verification!"
            message = "Hi " + fname + ". Welcome to Music App. Your OTP is " + str(otp)
            objemail.compose_mail(subject, message, email=email)
            
            objcreator.creator_insert(fname, lname, email, cname, password, path)
            flash("OTP was sent to your given email ID.")
            return redirect(url_for('otpverify', email=email))
        elif not bEmail:
            flash("This email ID already exists.")
            return redirect(url_for('creator_signup'))
        elif not bCname:
            flash("This username already exists.")
            return redirect(url_for('creator_signup'))
        else:
            flash("Creator already exists Please change the username and email ID.")
            return redirect(url_for('creator_signup'))
        
        # objcreator.creator_insert(fname, lname, email, cname, password, path)
        # flash("OTP was sent to your given email ID.")
        # return redirect(url_for('otpverify', email=email))
        # return render_template("creator_login.html")

@app.route("/creator_login", methods=["GET", "POST"])
def creator_login():
    if request.method == "GET":
        return render_template("creator_login.html")
    else:
        cname = request.form['cname']
        password = request.form['password']

        enc = encryption()
        password = enc.convert(password)

        r = objcreator.creator_login(cname, password)
        if r == 0:
            flash("Invalid username and password!")
            return redirect(url_for('creator_login'))
        else:
            # return "Welcome " + session['uname']
            return render_template('creator_dashboard.html')

# Creator dashboard
@app.route('/creator_dashboard', methods=["GET", "POST"])
def creator_dashboard():
    if 'cname' in session:
        if request.method == 'GET':
            return render_template('creator_dashboard.html')
    else:
        flash('Login to continue!')
        return render_template('creator_login.html')

# Creator profile
@app.route('/creator_profile', methods=["GET", "POST"])
def creator_profile():
    if 'cname' in session:
        if request.method == 'GET':
            record = objcreator.creator_profile()
            return render_template('creator_profile.html', record=record)
        elif request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            objcreator.creator_update(fname, lname)
            return redirect(url_for('creator_profile'))
    else:
        flash('Login to continue!')
        return redirect(url_for('creator_login'))

# Logout module
@app.route('/creator_logout', methods=["GET", "POST"])
def creator_logout():
    if 'cname' in session:
        if request.method=='GET':
            session.clear()
            flash("You are logged out!")
            return redirect(url_for("creator_login"))
    else:
        flash("You cannot access this page..please login")
        return redirect(url_for("creator_login"))

@app.route('/creator_audio',methods=['GET','POST'])
def creator_audio():
    if('cname' in session):
        if(request.method=='GET'):
            return render_template("creator_audio.html")
    else:
        flash("you can't access this page..please login to continue")
        return redirect(url_for('creator_login'))

@app.route('/creator_audioblog',methods=['GET','POST'])
def creator_audioblog():
    if('cname' in session):
        if(request.method=='GET'):
            lang = request.args.get('lang')
            category = request.args.get('category')
            try:
                audiolist = voice(lang)
                d = datetime.now()
                t=int(round(d.timestamp()))
                audio = str(t)+'.wav'
                with open('static/audioblog/' + audio,'wb') as f:
                    f.write(audiolist[1].get_wav_data())
                
                objcreator.creator_audioblog(audio, audiolist[0], category)
                flash("Your audio blog is recorded successfully!!")
                return redirect(url_for('creator_audio'))
            except Exception as e:
                flash(str(e))
                return redirect(url_for('creator_audio'))
            
        else:
            category = request.form['category']
            audio = request.files['audio']
        
            #------audio upload---------------------
            p = audio.filename
            if(p==''):
                flash("audio must be uploaded!!")
                return redirect(url_for('creator_audio'))
            d = datetime.now() #current date time
            t=int(round(d.timestamp()))
            path = str(t)+'.'+p.split('.')[-1]
            audio.save("static/audioblog/" + path)
            objcreator.creator_audio_upload(path, category)
            flash("Your audio blog is uploaded successfully!!")
            return redirect(url_for('creator_audio'))
    else:
        flash("you can't access this page..please login to continue")
        return redirect(url_for('creator_login'))
    
@app.route('/creator_get_uploaded',methods=['GET','POST'])
def creator_get_uploaded():
    if('cname' in session):
        if(request.method=='GET'):
            # Code to fetch all entries of a particular creator
            rows = objcreator.get_uploaded()
            return render_template("creator_uploaded.html", rows=rows)
    else:
        flash("you can't access this page..please login to continue")
        return redirect(url_for('creator_login'))
    
@app.route('/creator_get_recorded',methods=['GET','POST'])
def creator_get_recorded():
    if('cname' in session):
        if(request.method=='GET'):
            # Code to fetch all entries of a particular creator
            rows = objcreator.get_recorded()
            return render_template("creator_recorded.html", rows=rows)
    else:
        flash("you can't access this page..please login to continue")
        return redirect(url_for('creator_login'))
    
@app.route('/creator_delete_upload',methods=['GET','POST'])
def creator_delete_upload():
    if('cname' in session):
        if(request.method=='GET'):
            audioupload_id = int(request.args.get('audioupload_id'))
            objcreator.delete_upload(audioupload_id)
            flash("The uploaded audio was deleted!")
            return redirect(url_for('creator_get_uploaded'))
    else:
        flash("you can't access this page..please login to continue")
        return redirect(url_for('creator_login'))
    
@app.route('/creator_delete_audioblog',methods=['GET','POST'])
def creator_delete_audioblog():
    if('cname' in session):
        if(request.method=='GET'):
            audioblog_id = int(request.args.get('audioblog_id'))
            objcreator.delete_audioblog(audioblog_id)
            flash("The recorded audio was deleted!")
            return redirect(url_for('creator_get_recorded'))
    else:
        flash("you can't access this page..please login to continue")
        return redirect(url_for('creator_login'))

@app.route('/creator_edit_audio',methods=['GET','POST'])
def creator_edit_audio():
    if('cname' in session):
        if(request.method == 'GET'):
            audio_id = request.args.get('audio_id')
            record = objcreator.creator_edit_audio(audio_id)
            return render_template('creator_edit_audio.html',record=record) 
        else:
             audio_id=request.args.get('audio_id')
             category = request.form['category']
             objcreator.creator_audio_update(audio_id,category)
             flash('category changed successfully!!')
             return redirect(url_for('creator_get_recorded'))
    else:
        flash("you can't access this page..please login to continue")
        return redirect(url_for('creator_login')) 

@app.errorhandler(404)
def not_found(e):
    return "NOT FOUND"

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=5001)
