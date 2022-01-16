#!/usr/bin/env python

from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request,
    send_file
)
from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from app import create_app, db, login_manager, bcrypt
from models import User
from forms import login_form, register_form
import os


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()

UPLOAD_FOLDER = './files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'pptx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


@app.route("/<path:path>")
@app.route("/index")
@app.route("/")
@login_required
def index_2(path=""):
    direct = os.path.join(UPLOAD_FOLDER, path)
    entries = os.scandir(direct)
    return render_template("index.html", entries=entries)


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html", title="Home")


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
                           form=form,
                           text="Login",
                           title="Login",
                           btn_action="Login")


# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),)

            db.session.add(newuser)
            db.session.commit()
            flash("Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash("Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash("User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash("Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash("Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash("Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash("An error occured !", "danger")
    return render_template("auth.html",
                           form=form,
                           text="Create account",
                           title="Register",
                           btn_action="Register account")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/download_file/<path:path>")
@login_required
def download_file(path):
    return send_file(os.path.join(path))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index',
                                    filename=filename))
        return render_template("index.html")
    return render_template("upload.html")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True)
