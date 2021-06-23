from flask import Flask, render_template, url_for, redirect, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL1', "sqlite:///portfolio.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)

ADD_DELETE_KEY = os.environ.get('ADD_DELETE_KEY')


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    link_git = db.Column(db.String(250), nullable=False)
    link_product = db.Column(db.String(250), nullable=False)


db.create_all()


class KeyForm(FlaskForm):
    key = StringField('Enter the Key', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    img_url = StringField('Link to Image', validators=[DataRequired(), URL()])
    link_git = StringField('Link to GitHub', validators=[DataRequired(), URL()])
    link_product = StringField('Link to Product', validators=[DataRequired(), URL()])
    submit = SubmitField('Add')


class UpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    img_url = StringField('Link to Image', validators=[DataRequired(), URL()])
    link_git = StringField('Link to GitHub', validators=[DataRequired(), URL()])
    link_product = StringField('Link to Product', validators=[DataRequired(), URL()])
    submit = SubmitField('Update')


@app.route('/')
def home():
    all_posts = Post.query.all()
    return render_template('index.html', posts=all_posts)


@app.route('/security_key/<do>', methods=['GET', 'POST'])
def security(do):
    form = KeyForm()
    if form.validate_on_submit():
        if form.key.data == ADD_DELETE_KEY and do == 'delete':
            return redirect(url_for('delete', post_id=request.args.get('post_id')))
        elif form.key.data == ADD_DELETE_KEY and do == 'add':
            return redirect(url_for('add'))
        elif form.key.data == ADD_DELETE_KEY and do == 'update':
            return redirect(url_for('update', post_id=request.args.get('post_id')))
        else:
            flash('Wrong Key!')
    return render_template('secret.html', form=form)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    delete_post = Post.query.get(post_id)
    db.session.delete(delete_post)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        new_post = Post(name=form.name.data, description=form.description.data, img_url=form.img_url.data,
                        link_git=form.link_git.data, link_product=form.link_product.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form, label_add=True)


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = Post.query.get(post_id)
    form = UpdateForm(name=post.name, description=post.description, img_url=post.img_url, link_git=post.link_git,
                      link_product=post.link_product)
    if form.validate_on_submit():
        post.name = form.name.data
        post.description = form.description.data
        post.img_url = form.img_url.data
        post.link_git = form.link_git.data
        post.link_product = form.link_product.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form, label_add=False)


if __name__ == '__main__':
    app.run(debug=True)
