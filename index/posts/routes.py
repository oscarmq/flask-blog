from flask import render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from index.models import Post
from index.posts.forms import PostForm
from index import db
from flask import Blueprint

posts = Blueprint('posts', __name__)


@posts.route("/post/create", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.', category='success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='Create Post', form=form)
