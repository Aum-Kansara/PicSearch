from flask import Flask,render_template,request,redirect


app=Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def loginPage():
    return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signUpPage():
    return render_template("signup.html")

@app.route("/reset",methods=["GET","POST"])
def resetPassword():
    return render_template("reset.html")

@app.route("/user",methods=["GET","POST"])
def userPage():
    return render_template("eventcode.html")

if __name__=="__main__":
    app.run(debug=True)