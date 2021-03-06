from flask import Flask, request, redirect, render_template
import re

app = Flask(__name__)
app.config['DEBUG'] = True

username = ""
email = ""

def verify_email_validity(email):
    error = ""
    email.strip()
    if len(email) > 2 and len(email) < 21 : #something there
        if len(re.findall(r"@", email)) != 1:
            error = "Email is not valid, not a single @"
        if len(re.findall(r"\.", email)) != 1:
            error = "Email is not valid, not a single '.'"
        if len(re.findall(r" ", email)) == 1 or len(re.findall(r" ", email)) > 1:
            error = "Email is not valid, has a space"
    elif len(email) == 0:
        error = ""
    elif len(email) < 3 and len(email) != 0:
        error = "Email is not valid, not between 3 and 20 characters. Clear field for no email submission"
    return error

def verify_username_validity(username):
    error = ""
    username.strip()
    if len(username) > 3 and len(username) < 20:
        if len(re.findall(r" ",username)) > 0:
            error = "Username is not valid, has a space"
    elif len(username)==0:
        error = "Username not entered"
    else:
        error = "Username is not valid, must be between 3 and 20 characters"

    return error

def verify_password_validity(password,verify_password):
    error = ""
    pattern = re.compile(password)
    if len(password) > 2 and len(password) < 21:
        if pattern.match(verify_password) == False:
            error = "Password and verification do not match"
        if len(re.findall(r" ",password)) > 0:
            error = "Username is not valid, has a space"
    elif len(password) < 3 or len(password)>21:
        error = "Password must be between 3 and 20 characters long and have no spaces"
    else:
        error = "Password must be between 3 and 20 characters long and have no spaces"

    return error

@app.route("/",methods=["GET"])
def index():
    if request.method == "GET":
        errorEmail = request.args.get("errorEmail")
        print(errorEmail)
        errorUsername = request.args.get("errorUsername")
        print(errorUsername)
        errorPassword = request.args.get("errorPassword")
        print(errorPassword)
        username = request.args.get("username")
        email = request.args.get("email")
        if errorEmail == None:
            errorEmail = ""
        if errorPassword == None:
            errorPassword = ""
        if errorUsername == None:
            errorUsername = ""
        if email == None:
            email = ""
        if username == None:
            username = ""
        return render_template('index.html',errorEmail = errorEmail,errorPassword=errorPassword,errorUsername=errorUsername,email=email,username=username)
    else:
        if email == None:
            email = ""
        if username == None:
            username = ""
        return render_template('index.html',email=email,username=username)
	
@app.route("/welcome",methods=['POST'])
def welcome():
    username = request.form["username"]
    password = request.form["password"]
    verify_password = request.form["verify_password"]
    email = request.form["email"]
    
    errorUsername = verify_username_validity(username)
    errorPassword = verify_password_validity(password,verify_password)
    errorEmail = verify_email_validity(email)

    print(errorUsername)
    print(errorPassword)
    print(errorEmail)

    redirectString = "/"
    if errorUsername:
        if len(redirectString) == 1:   
            redirectString = redirectString + "?errorUsername=" + errorUsername
        else:
            redirectString = redirectString + "&errorUsername=" + errorUsername
    if errorPassword:
        if len(redirectString) == 1:
            redirectString = redirectString + "?errorPassword=" + errorPassword
        else:
            redirectString = redirectString + "&errorPassword=" + errorPassword
    if errorEmail:
        if len(redirectString) == 1:
            redirectString = redirectString + "?errorEmail=" + errorEmail
        else:
            redirectString = redirectString + "&errorEmail=" + errorEmail
    if len(redirectString) == 1:
        return render_template('welcome.html',username = username)
    if len(redirectString) > 1:
        redirectString = redirectString + "&username=" + username + "&email=" + email
        return redirect(redirectString)
   
	
	
if __name__ == "__main__":
    app.run()