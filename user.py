from flask import session
import mysql.connector as msc

class UserOperation:
    def connection(self):
        conn = msc.connect(host='localhost', port='3306', user='root', password='password', database='ca590_project')
        return conn
    
    def user_check_email(self, email):
        db = self.connection()
        mycursor = db.cursor()
        query_email = "select email from user_login_signup where email=%s;"
        record = [email]
        mycursor.execute(query_email, record)
        rows = mycursor.fetchall()
        rc = mycursor.rowcount

        if rc == 0:
            return False
        else:
            return True

    def user_check_uname(self, uname):
        db = self.connection()
        mycursor = db.cursor()
        query_uname = "select uname from user_login_signup where uname=%s;"
        record = [uname]
        mycursor.execute(query_uname, record)
        rows = mycursor.fetchall()
        rc = mycursor.rowcount

        if rc == 0:
            return False
        else:
            return True

    def user_insert(self, fname, lname, email, uname, password):
        db = self.connection()
        mycursor = db.cursor()

        query = "insert  into user_login_signup(fname, lname, email, uname, password) values (%s, %s, %s, %s, %s);"

        record=[fname, lname, email, uname, password]
        mycursor.execute(query, record)

        db.commit()

        mycursor.close()
        db.close()

    def user_delete(self,email):
        db = self.connection()
        mycursor = db.cursor()
        sq = "delete from user where email=%s"
        record=[email]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def user_login(self,uname, password):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select fname, uname from user_login_signup where uname=%s and password=%s;"
        record=[uname, password]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        rc = mycursor.rowcount
        mycursor.close()
        db.close()
        if rc == 0:
            return 0
        else:
            session['fname']=row[0][0]
            session['uname']=row[0][1]
            return 1
