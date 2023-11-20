from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user

from app import app
from . import post_blueprint
from .models import db, Post
from .forms import CreatePostForm

import os
import secrets
from PIL import Image

@post_blueprint.route("/", methods=['GET', 'POST'])
@login_required
def view_post():
    all_posts = Post.query.all()
    image_file = url_for('static', filename='images/')

    return render_template('post.html', all_posts=all_posts, image_file=image_file)

@post_blueprint.route("/<int:user_id>", methods=['GET', 'POST'])
def detail_post(user_id=None):
    get_post = Post.query.get_or_404(user_id)
    return render_template('detail_post.html', pk=get_post)

@post_blueprint.route("/create", methods=['POST'])
@login_required
def create():
    form = CreatePostForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            image = picture_file
        else:
            image = 'postdefault.jpg'

        new_post = Post(title=form.title.data, text=form.text.data, type=form.type.data, image_file=image, post_id=current_user.id)
        
        db.session.add(new_post)
        db.session.commit()
        flash("Створення виконано", category=("success"))
        return redirect(url_for("post.view_post"))
    
    flash("Помилка при створенні", category=("danger"))
    return redirect(url_for("post.view_post"))

@post_blueprint.route("/update_todo/<int:user_id>")
def update(user_id=None):
    get_post = Post.query.get_or_404(user_id)
    if current_user.id != get_post.post_id:
        flash("Це не ваш пост", category=("warning"))
        return redirect(url_for('post.view_detail', user_id=user_id))
    
    form = CreatePostForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            get_post.image_file = picture_file

        get_post.title = form.title.data
        get_post.text = form.text.data
        get_post.type = form.type.data

        db.session.commit()
        db.session.add(get_post)

        flash("Пост був доданий", category=("access"))
        return redirect(url_for('post.view_detail', user_id=user_id))

    form.title.data = get_post.title
    form.text.data = get_post.text
    form.type.data = get_post.type

    return redirect(url_for("post.view_post"))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@post_blueprint.route("/delete_todo/<int:user_id>")
def delete(user_id=None):
    get_post = Post.query.get_or_404(user_id)

    if current_user.id == get_post.post_id:
        db.session.delete(get_post)
        db.session.commit()
        flash("Видалення виконано", category=("success"))

    flash("Це не ваш пост", category=("warning"))
    return redirect(url_for('post.view_detail', user_id=user_id))