from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user

from app import app
from . import post_blueprint
from .models import db, Post, Category
from .forms import CreatePostForm

import os
import secrets
from PIL import Image

@post_blueprint.route("/", methods=['GET', 'POST'])
@login_required
def view_post():
    all_posts = Post.query.all()
    image_file = url_for('static', filename='images/')

    return render_template('show_all_posts.html', all_posts=all_posts, image_file=image_file)

@post_blueprint.route("/<int:id>", methods=['GET', 'POST'])
def view_detail(id):
    get_post = Post.query.get_or_404(id)
    return render_template('detail_post.html', pk=get_post)

@post_blueprint.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePostForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            image = picture_file
        else:
            image = 'postdefault.png'

        new_post = Post(title=form.title.data, text=form.text.data, type=form.type.data, image_file=image, user_id=current_user.id)
        
        db.session.add(new_post)
        db.session.commit()
        flash("Створення виконано", category=("success"))
        return redirect(url_for("post_bp.view_post"))
    
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    return render_template('create_post.html', form=form)

@post_blueprint.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    get_post = Post.query.get_or_404(id)
    if current_user.id != get_post.user_id:
        flash("Це не ваш пост", category=("warning"))
        return redirect(url_for('post_bp.view_detail', id=id))
    
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

        flash("Пост був оновлений", category=("access"))
        return redirect(url_for('post_bp.view_detail', id=id))

    form.title.data = get_post.title
    form.text.data = get_post.text
    form.type.data = get_post.type

    return render_template('update_post.html', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'post/static/post/images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@post_blueprint.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    get_post = Post.query.get_or_404(id)

    if current_user.id == get_post.user_id:
        db.session.delete(get_post)
        db.session.commit()
        flash("Видалення виконано", category=("success"))
    else:
        flash("Це не ваш пост", category=("warning"))

    return redirect(url_for('post_bp.view_post'))