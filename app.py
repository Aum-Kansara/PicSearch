from flask import Flask,render_template,request,redirect,session,g,url_for
from sqlite3 import connect
import os
from werkzeug.utils import secure_filename
from generate_code import generateEventCode
from threading import Thread
from add_faces import processDatasetImages,processKnownPeopleImages
from email_sender import send_email

app=Flask(__name__)
app.config['UPLOAD_FOLDER']='static/uploads'
app.secret_key=os.urandom(24)


        
def main():
    """
    Main Function.
    Returns
    -------
    None.
    """
    datasetPath="./static/event/maniac_week"
    peoplePath="./static/uploads/"
    processKnownPeopleImages(path=peoplePath)
    processDatasetImages(path=datasetPath)
    print("Completed")
    send_email("aumkan23@gmail.com",'static/events/maniac_week')

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")



@app.route("/auth",methods=["GET","POST"])
def authenticate():
    if g.user:
        return render_template("eventcode.html",user=session['user'])
    return redirect('/login')

@app.route("/eauth",methods=["GET","POST"])
def eauthenticate():
    if g.user:
        conn=connect('users.db')
        user=session['user']
        data = conn.execute(f"select name,event_name,event_code from event_manager where eid='{user}'").fetchall()
        return render_template("admin.html",user=session['user'],name=data[0][0],event_name=data[0][1],event_code=data[0][2])
    return redirect('/elogin')

@app.route("/verify",methods=["GET","POST"])
def verifyEventCode():
    if request.method=="POST":
        conn=connect('users.db')
        code=request.form.get("event-code")
        if code!=None:
            data = conn.execute(f"select event_code from event_manager where event_code='{code}'")
        if len(data.fetchall())>0:
            return render_template("upload.html",event_id=code)
        else:
            return render_template('eventcode.html',code_error='incorrect')
    return redirect('/auth')
        

@app.route("/login",methods=["GET","POST"])
def loginPage():
    if g.user:
        return redirect('/auth')
    if request.method=="POST":
        session.pop('user',None)
        conn=connect('users.db')
        data = conn.execute(f"select Id,pass from USERS where email='{request.form.get('email')}'")
        result=data.fetchall()
        if result!=[]:
            if request.form.get("password")==result[0][1]:
                session['user']=result[0][0]
                return redirect('/auth')
            else:
                return render_template("login.html")
    return render_template("login.html")

@app.route("/elogin",methods=["GET","POST"])
def eloginPage():
    if request.method=="POST":
        session.pop('user',None)
        conn=connect('users.db')
        data = conn.execute(f"select eid,pass,event_code from event_manager where email='{request.form.get('email')}'")
        result=data.fetchall()
        if result!=[]:
            if request.form.get("password")==result[0][1]:
                session['user']=result[0][0]
                return redirect('/eauth')
            else:
                return render_template("event_manager.html",name=result[0][0],event_name=result[0][1],event_code=result[0][1])
    return render_template("event_manager.html")



@app.route("/signup",methods=["GET","POST"])
def signUpPage():
    if request.method=="POST":
        conn=connect('users.db')
        conn.execute(f"insert into Users(name,email,pass) values('{request.form.get('name')}','{request.form.get('email')}','{request.form.get('password')}')")
        conn.commit()
        conn.close()
        print("Succesfully Added Data")
        return render_template("login.html")
    return render_template("signup.html")

@app.route("/esignup",methods=["GET","POST"])
def esignUpPage():
    if g.user:
        return redirect('eauth')
    if request.method=="POST":
        conn=connect('users.db')
        code=generateCode()
        conn.execute(f"insert into event_manager(name,email,pass,event_name,event_code) values('{request.form.get('name')}','{request.form.get('email')}','{request.form.get('password')}','{request.form.get('event-name')}','{code}')")
        conn.commit()
        conn.close()
        print("Succesfully Added Data")
        return render_template("event-manager.html",user_name=session['user'])
    return render_template("event_manager_signup.html")

@app.route("/reset",methods=["GET","POST"])
def resetPassword():
    return render_template("reset.html")

@app.route("/user",methods=["GET","POST"])
def userPage():
    return render_template("eventcode.html")

@app.route("/upload_page",methods=["GET","POST"])
def uploadPage():
    return render_template('upload.html')

@app.route("/add_drive",methods=["GET","POST"])
def addDriveLink():
    if request.method=="POST":
        code=request.form.get('drive')
        conn=connect('users.db')
        eid=session['user']
        conn.execute(f"UPDATE event_manager set photos_link = ? where eid = ?",(code,eid))
        conn.commit()
        session['user']=None
        return f"<h1>Link Added Succesfully</h1>"
    return render_template('upload.html')


@app.route("/generateEventCode",methods=["GET","POST"])
def generateCode():
    if request.method=="POST":
        code=generateEventCode()
        conn=connect('users.db')
        eid=session['user']
        conn.execute(f"UPDATE event_manager set event_code = ? where eid = ?",(code,eid))
        conn.commit()
        return f"<h1>Generated Code is {code}</h1>"
    return redirect('eauth')

@app.route("/upload",methods=["GET","POST"])
def uploadImage():
    if request.method=="POST":
        f=request.files['file']
        conn=connect('users.db')
        user_id=session['user']
        data = conn.execute(f"select name from USERS where id='{user_id}'")
        name=data.fetchall()
        if name!=[]:
            photo_id=len(os.listdir(app.config['UPLOAD_FOLDER']))+1
            img_path=os.path.join(app.config['UPLOAD_FOLDER'],f"{name[0]}_{photo_id}_"+secure_filename(f.filename))
            f.save(img_path)
            code=request.form.get('event_id')
            event_name=conn.execute(f'select event_name from event_manager where event_code="{code}"').fetchall()[0][0]
            Thread(target=main).start()
            return f"Mailing Your Photos from {event_name} in 2 to 5 minutes"

    return redirect('/auth')

@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user']

if __name__=="__main__":
    app.run(debug=True)