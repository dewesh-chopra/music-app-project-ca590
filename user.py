from datetime import datetime
from flask import session
from encryption import encryption
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

    def user_delete(self,uname):
        db = self.connection()
        mycursor = db.cursor()
        sq = "delete from user_login_signup where uname=%s"
        record=[uname]
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
    
    def user_match_password(self, uname, password):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select password from user_login_signup where uname=%s;"
        record=[uname]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        print(row[0][0])
        if row[0][0] == password:
            return True
        else:
            return False
    
    def user_change_password(self, uname, password):
        db = self.connection()
        mycursor = db.cursor()
        sq = "update user_login_signup set password=%s where uname=%s;"
        record=[password, uname]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def user_update(self, fname, lname):
        db = self.connection()
        mycursor = db.cursor()
        sq = "update user_login_signup set fname=%s, lname=%s where uname=%s;"
        record=[fname, lname, session['uname']]
        mycursor.execute(sq,record)
        db.commit()
        session['fname']=fname
        mycursor.close()
        db.close()
        return
        
    def user_profile(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select fname, lname, uname, email, password from user_login_signup where uname=%s;"
        record=[session['uname']]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def user_blog_listen(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select id, category, title, audio from audioblog;"
        mycursor.execute(sq)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def user_song_listen(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select id, category, title, audio from audio_upload;"
        mycursor.execute(sq)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def user_search_song(self, search_term):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select id, category, title, audio from audio_upload where title like %s;"
        record=['%' + search_term + '%']
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def user_search_blog(self, search_term):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select id, category, title, audio from audioblog where title like %s;"
        record=['%' + search_term + '%']
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def user_song_view(self, audio_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "SELECT audio_upload.title, audio_upload.created_at, audio_upload.category, audio_upload.audio, creator_login_signup.fname, creator_login_signup.lname FROM audio_upload JOIN creator_login_signup ON audio_upload.creator_id = creator_login_signup.id WHERE audio_upload.id = %s;"
        record = [audio_id]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def user_blog_view(self, audio_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "SELECT audioblog.title, audioblog.created_at, audioblog.category, audioblog.audio, audioblog.audiotext, creator_login_signup.fname, creator_login_signup.lname FROM audioblog JOIN creator_login_signup ON audioblog.creator_id = creator_login_signup.id WHERE audioblog.id = %s;"
        record = [audio_id]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def user_playlist_collection(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "SELECT playlist_name FROM playlist_collection WHERE user_name = %s;"
        record = [session['uname']]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def user_add_playlist_collection(self, playlist_name):
        db = self.connection()
        mycursor = db.cursor()
        sq = "INSERT INTO playlist_collection (user_name, playlist_name) values (%s, %s);"
        record = [session['uname'], playlist_name]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def user_add_playlist(self, playlist_name, audio_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "INSERT INTO playlist (user_name, playlist_name, audio_id) values (%s, %s, %s);"
        record = [session['uname'], playlist_name, audio_id]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def get_blog_review(self,audio_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select user_name, comment, star, created_at from review_blog where blog_id=%s;"
        record=[audio_id]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def submit_blog_review(self,audioblog_id,comment,star):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into review_blog(blog_id,user_name,comment,star,created_at)values(%s,%s,%s,%s,%s)"
        record=[audioblog_id,session['uname'],comment,star,datetime.now()]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def get_song_review(self,audio_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select user_name, comment, star, created_at from review_song where song_id=%s;"
        record=[audio_id]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def submit_song_review(self,audio_id,comment,star):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into review_song(song_id,user_name,comment,star,created_at)values(%s,%s,%s,%s,%s)"
        record=[audio_id,session['uname'],comment,star,datetime.now()]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return
