from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor, CKEditorField
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
gravatar = Gravatar(app,
                    size=35,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    comments = relationship("Comment", back_populates='cauthor')
    posts = relationship("BlogPost", back_populates="author")

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = relationship("Comment", back_populates='blogpost')

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    cauthor = relationship("User", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    blogpost = relationship("BlogPost", back_populates='comments')
    text = db.Column(db.Text, nullable=False)

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    # author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class CommentForm(FlaskForm):
    body = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("SUMBIT COMMENT!")

    
# Create all the tables in the database
db.create_all()

# db.session.add(BlogPost(author_id=1, title='The Life of Cactus', subtitle='Who Knew That cacti lived such interesting lives', body='Cactus is a unique plant. It stores a large amount of water, which allows it to survive extreme temperatures. Almost all cacti are native to hot and dry habitats of South and North America. There are almost 2000 different species of cacti. However, being a very attractive plant that comes in all shapes, sizes, and colors, cactus become a wildly popular house and garden plant all around the world. Therefore, habitat loss and over-collecting are big treats to cacti surviving in the wild. Because of that, certain species are listed as endangered and trading of most cacti species is forbidden by the law.', date='July 13, 2022', author='Veer Rajput', img_url='https://www.nwf.org/Educational-Resources/Wildlife-Guide/Plants-and-Fungi/Cacti'))
# db.session.add(BlogPost(title='Top 10 Things to do When You are Bored', subtitle="Are you bored? Don't know what to do? Try these top 10 activities.", body='1: Play video games. 2: Play catch. 3. Go swimming. 4. Play basketball. 5. Play Cricket. 6. Learn coding. 7. Go shopping. 8. Eat candy. 9. Watch insane youtube videos. 10. Watch movies', date='July 13, 2022', img_url='https://www.nwf.org/Educational-Resources/Wildlife-Guide/Plants-and-Fungi/Cacti'))
# db.session.add(BlogPost(title='Top 10 Nintendo games', subtitle='Learn about the top ten nintendo games of all time.', body='1. The Legend of Zelda: Breath of the Wild. 2. Super Mario Odyssey. 3. Animal Crossing: New Horizons. 4. Splatoon 2. 5. Super Smash Bros Ultimate. 6. Mario Kart 8 Deluxe. 7. Super Mario Maker 2. 8. Kirby and the Forgotten Land. 9. Rayman Legends Definitive Edition. 10. Mario + Rabbids Kingdom Battle', date='July 13, 2022', img_url='https://www.nwf.org/Educational-Resources/Wildlife-Guide/Plants-and-Fungi/Cacti'))
# db.session.commit()



def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)        
    return decorated_function

print(current_user)



@app.route('/')
def get_all_posts(*args):
    # print(args)
    # try:
    #     if args[0] == True:
    #         current_user = args[0]
    # except:
    #     pass
    # db.session.add(BlogPost(author_id=1, title='The Life of Cactus', subtitle='Who Knew That cacti lived such interesting lives', body='Cactus is a unique plant. It stores a large amount of water, which allows it to survive extreme temperatures. Almost all cacti are native to hot and dry habitats of South and North America. There are almost 2000 different species of cacti. However, being a very attractive plant that comes in all shapes, sizes, and colors, cactus become a wildly popular house and garden plant all around the world. Therefore, habitat loss and over-collecting are big treats to cacti surviving in the wild. Because of that, certain species are listed as endangered and trading of most cacti species is forbidden by the law.', date='July 13, 2022', img_url='https://www.nwf.org/Educational-Resources/Wildlife-Guide/Plants-and-Fungi/Cacti'))
    # db.session.commit()
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts, current_user=current_user)

@login_required
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, h1='New Post', current_user=current_user)

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def show_post(post_id):
    form = CommentForm(body='')
    requested_post = BlogPost.query.get(post_id)
    if form.validate_on_submit():
        new_comment = Comment(
            text=form.body.data,
            cauthor=current_user,
            blogpost=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    comments = requested_post.comments
    return render_template("post.html", post=requested_post, current_user=current_user, form=form)


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)

@app.route("/edit-post/<post_id>", methods=["GET","POST"])
@login_required
@admin_only
def edit(post_id):
    post = BlogPost.query.get(post_id)
    form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.author = current_user
        post.img_url = form.img_url.data
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", h1='Edit Post', form=form, current_user=current_user)

@admin_only
@login_required
@app.route("/delete/<post_id>")
def delete(post_id):
    post = BlogPost.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))

@app.route("/register", methods=["GET", "POST"])
def register():
    current_user=None
    form = RegisterForm()
    if form.validate_on_submit():
        password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=12
        )
        
        if User.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        
        new_user = User(email=form.email.data, password=password, name=form.name.data)
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form, current_user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    current_user=None
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
    
        user = User.query.filter_by(email=email).first()
        #Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template('login.html', form=form)



@app.route("/logout")
def logout():
    current_user=None
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts, current_user=current_user)
    # return redirect(url_for('get_all_posts', user=current_user))

if __name__ == "__main__":
    app.run(debug=True, port=5000)