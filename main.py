from flask import Flask, request, redirect, render_template
import re

app = Flask(__name__)
app.config['DEBUG'] = True

def verify_email_validity(email):
    error = []
    if len(email) > 3 and len(email) < 20 : #something there
        if len(re.findall(r"@", email)) != 1:
            error = "Email is not valid, not a single @"
        if len(re.findall(r".", email)) != 1:
            error = "Email is not valid, not a single ."
        if len(re.findall(r" ", email)) != 1:
            error = "Email is not valid, has a space"
    elif len(email) == 0:
        error = []
    else:
        error = "Email is not valid, not between 3 and 20 characters"
    return error

def verify_username_validity(username):
    error = []
    if len(username) > 3 and len(username) < 20:
        if len(re.findall(r" ",username)) > 0:
            error = "Username is not valid, has a space"
    elif len(username)==0:
        error = "Username not entered!"

    return error

def verify_password_validity(password,verify_password):
    error = []
    pattern = re.compile(password)
    if len(password) > 3 and len(password) < 20:
        if pattern.match(verify_password) == False:
            error = "Password and verification do not match!"
    else:
        error = "Password must be between 3 and 20 characters long"

    return error

@app.route("/",methods = ["GET"])
def index():
    error = request.args.get("error")
    return render_template('index.html')
	
@app.route("/welcome",methods=['POST'])
def welcome():
    username = request.form["username"]
    password = request.form["password"]
    verify_password = request.form["verify_password"]
    email = request.form["email"]
	
    errorUsername = verify_username_validity(username)
    errorPassword = verify_password_validity(password,verify_password)
    errorEmail = verify_email_validity(email)

    errors = [errorUsername,errorPassword,errorEmail]

    return render_template('welcome.html',username = username)
	
	
if __name__ == "__main__":
    app.run()