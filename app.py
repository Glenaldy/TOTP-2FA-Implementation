from flask import Flask, flash, message_flashed, redirect, render_template, request, session, url_for
import CustomOTP
import CustomDB


app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
user_db = "users.json"

# Login Page


@app.route('/', methods=["GET", "POST"])
def login_page():
    # Get method request
    if request.method == "GET":
        return render_template('login.html')

    # Post method request
    if request.method == 'POST':
        users_list = CustomDB.get_users_data(user_db)
        username = request.form.get("username")
        password = request.form.get("password")

        user = CustomDB.find_user(users_list, username, password)
        if user:
            session["user"] = user
            return redirect(url_for('login_2fa'))
        else:
            flash("Invalid login", "danger")
            return redirect(url_for('login_page'))


# Two-Factor Authentication Page
@app.route('/login2fa', methods=["GET", "POST"])
def login_2fa():
    secret_key = session["user"]["secret_key"]

    # Insert randomly generated secret_key into database if empty
    if secret_key == "":
        secret_key = new_secret_key(session["user"])["secret_key"]

    # Generate new URI for Google Authenticator
    uri = CustomOTP.generate_uri(
        secret_key, session["user"]["username"], "KCGI_Information_Security")
    CustomOTP.generate_qr(uri, "static/qr.png")

    # Get method request
    if request.method == "GET":
        return render_template("twofactorauthentication.html", secret_key=secret_key)

    # Post method request for
    if request.method == "POST":
        # Request to authenticate secret key
        if "authenticate_secret" in request.form:
            otp = request.form.get("otp")
            if CustomOTP.verify(secret_key, int(otp)):
                # OTP Valid
                flash("The TOTP 2FA token is valid", "success")
                return redirect(url_for("login_2fa"))
            else:
                # OTP Invalid
                flash("Invalid 2FA token", "danger")
                return redirect(url_for("login_2fa"))

        # Request to generate new secret key
        elif "generate_secret" in request.form:
            session["user"] = new_secret_key(session["user"])
            secret_key = session["user"]["secret_key"]
            uri = CustomOTP.generate_uri(
                secret_key, session["user"]["username"], "KCGI_Information_Security")

            CustomOTP.generate_qr(uri, "static/qr.png")

            flash("New secret key generated", "warning")
            return redirect(url_for("login_2fa"))


def new_secret_key(session_user):
    secret_key = CustomOTP.generate_secret_key()
    session["user"]["secret_key"] = secret_key
    session_user = CustomDB.insert_new_secret_key(user_db, session_user)
    return session_user
