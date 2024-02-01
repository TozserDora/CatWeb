from flask import Flask, flash, request, render_template, redirect, url_for
from forms import SignUpForm, LogInForm, UploadForm
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
import os
from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ.get("SECRETKEY")
ckeditor = CKEditor(app)


# Create the database
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.context_processor
def inject_user():
    return dict(current_user=current_user)


# Create cat_posts table
class CatPost(db.Model):
    __tablename__ = "cat_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    # author = relationship("User", back_populates="posts")
    # comments = relationship("Comment", back_populates="parent_post")


# Create users table
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


# Home page with all posts
@app.route('/')
def home():
    result = db.session.execute(db.select(CatPost))
    posts = result.scalars().all()
    return render_template('index.html', all_posts=posts)


@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        password = form.password.data
        password_2 = form.password_2.data

        if password == password_2:
            password_hashed_salted = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
            new_user = User(
                username=form.user.data,
                email=form.email.data,
                password=password_hashed_salted
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
        else:
            return render_template('signup.html', form=form)

    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def log_in():
    form = LogInForm()
    if form.validate_on_submit():
        email = form.email.data
        typed_password = form.password.data

        # Find user by email
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        # Check stored password hash against entered password hashed.
        if user and check_password_hash(user.password, typed_password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password. Please try again.")
    return render_template('login.html', form=form)


@app.route('/logout')
def log_out():
    logout_user()
    return redirect(url_for('home'))


# Upload picture with title and description --> Add to database
@app.route('/upload', methods=["POST", "GET"])
def upload_picture():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.photo.data
        filename = secure_filename(file.filename)
        date_string = str(dt.now()).replace(".", "-")[0]
        full_name = date_string + filename
        path = "static/uploads/" + full_name
        file.save(path)
        new_post = CatPost(
            title=form.title.data,
            description=form.description.data,
            date=dt.now().strftime("%B %d, %Y"),
            img_url=path
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('upload.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)