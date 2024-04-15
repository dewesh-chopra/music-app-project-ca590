from datetime import datetime
from flask import session
from encryption import encryption
import mysql.connector as msc

class CreatorOperation:
    def connection(self):
        conn = msc.connect(host='localhost', port='3306', user='root', password='password', database='ca590_project')
        return conn
    
    def creator_insert(self, fname, lname, email, cname, password, photo):
        db = self.connection()
        mycursor = db.cursor()

        query = "insert  into creator_login_signup(fname, lname, email, cname, password, photo) values (%s, %s, %s, %s, %s, %s);"

        record=[fname, lname, email, cname, password, photo]
        mycursor.execute(query, record)

        db.commit()

        mycursor.close()
        db.close()

    def creator_update(self, fname, lname):
        db = self.connection()
        mycursor = db.cursor()
        sq = "update creator_login_signup set fname=%s, lname=%s where cname=%s;"
        record=[fname, lname, session['cname']]
        mycursor.execute(sq,record)
        db.commit()
        session['fname']=fname
        mycursor.close()
        db.close()
        return

    def creator_login(self, cname, password):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select fname, cname, id from creator_login_signup where cname=%s and password=%s;"
        record=[cname, password]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        rc = mycursor.rowcount
        mycursor.close()
        db.close()
        if rc == 0:
            return 0
        else:
            session['fname']=row[0][0]
            session['cname']=row[0][1]
            session['creator_id']=row[0][2]
            return 1
        
    def creator_profile(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select fname, lname, cname, email, password, photo from creator_login_signup where cname=%s;"
        record=[session['cname']]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def creator_check_email(self, email):
        db = self.connection()
        mycursor = db.cursor()
        query_email = "select email from creator_login_signup where email=%s;"
        record = [email]
        mycursor.execute(query_email, record)
        rows = mycursor.fetchall()
        rc = mycursor.rowcount

        if rc == 0:
            return False
        else:
            return True

    def creator_check_cname(self, cname):
        db = self.connection()
        mycursor = db.cursor()
        query_cname = "select cname from creator_login_signup where cname=%s;"
        record = [cname]
        mycursor.execute(query_cname, record)
        rows = mycursor.fetchall()
        rc = mycursor.rowcount

        if rc == 0:
            return False
        else:
            return True

    def creator_delete(self, cname):
        db = self.connection()
        mycursor = db.cursor()
        sq = "delete from creator_login_signup where cname=%s"
        record=[cname]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def creator_audioblog(self,audio,audiotext, category):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into audioblog(creator_id,audio,audiotext,category, created_at) values (%s,%s,%s,%s, %s);"
        created_at = datetime.now()
        record=[session['creator_id'],audio,audiotext, category,created_at]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def creator_audio_upload(self,path, category):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into audio_upload (creator_id,audio, category,created_at) values (%s,%s,%s,%s)"
        created_at = datetime.now()
        record=[session['creator_id'],path,category,created_at]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def get_uploaded(self):
        db = self.connection()
        mycursor = db.cursor()
        query = "select id, category, audio from audio_upload where creator_id=%s;"
        record = [session['creator_id']]
        mycursor.execute(query, record)
        rows = mycursor.fetchall()
        mycursor.close()
        db.close()
        return rows
        
    def get_recorded(self):
        db = self.connection()
        mycursor = db.cursor()
        query = "select id, audio, audiotext, category from audioblog where creator_id=%s;"
        record = [session['creator_id']]
        mycursor.execute(query, record)
        rows = mycursor.fetchall()
        mycursor.close()
        db.close()
        return rows
        
    def delete_audioblog(self, audioblog_id):
        db = self.connection()
        mycursor = db.cursor()
        query = "delete from audioblog where id=%s;"
        record = [audioblog_id]
        mycursor.execute(query, record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def delete_upload(self, audioupload_id):
        db = self.connection()
        mycursor = db.cursor()
        query = "delete from audio_upload where id=%s;"
        record = [audioupload_id]
        mycursor.execute(query, record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def creator_edit_audio(self, audio_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select category from audioblog where id=%s"
        record=[audio_id]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def creator_audio_update(self, audio_id, category):
        db = self.connection()
        mycursor = db.cursor()
        sq = "update audioblog set category=%s where id=%s"
        record=[category, audio_id]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return
