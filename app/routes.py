from datetime import datetime

import boto3
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db
from flask import render_template, flash, redirect, url_for, request, send_file, Response
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddTagForm, UploadFileForm, TagsForm
from flask_login import current_user, login_user, login_required
from app.models import User, Tag, File
from flask_login import logout_user
from sqlalchemy_utils import Ltree

BUCKET = 'oob-bucket'


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Oleg'}
    return render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        print('User', user)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/tags', methods=['GET', 'POST'])
@login_required
def tags_page():
    form = TagsForm()
    tag = Tag.query.filter_by(name='root').first()

    if request.method == 'POST':
        id = form.parent.data
        if id is None:
            flash('Choose parent')
            return redirect(url_for('tags_page'))

        flash('Parent {} was selected'.format(id))
        return redirect(url_for('tags_page'))

    return render_template('tags.html', tag=tag, form=form)


@app.route('/add_tag', methods=['GET', 'POST'])
@login_required
def add_tag():
    parent_id = request.args.get('parent_id')

    if parent_id is None:
        return redirect(url_for('tags_page'))

    form = AddTagForm()

    if form.validate_on_submit():
        parent = Tag.query.get(parent_id)
        print(parent)
        tag = Tag(name=form.name.data, path=Ltree(str(parent.path) + '.' + form.name.data))
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('tags_page'))

    return render_template('add_tag.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadFileForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        f = form.file.data
        mimetype = f.mimetype

        s3 = boto3.client('s3')
        s3.upload_fileobj(f, BUCKET, filename)

        file = File(url=filename, file_type='pdf', mimetype=mimetype)
        db.session.add(file)
        db.session.commit()

        return redirect(url_for('files'))

    return render_template('upload.html', form=form)


@app.route('/files')
def files():
    _files = File.query.all()
    return render_template('files.html', files=_files)


@app.route('/download')
def download():
    id = request.args.get('id')

    file = File.query.get(int(id))

    s3 = boto3.client('s3')

    s3_response_object = s3.get_object(Bucket=BUCKET, Key=file.url)
    object_content = s3_response_object['Body'].read()

    print('content', object_content)
    return Response(
        object_content,
        mimetype=file.mimetype,
        headers={"Content-Disposition": "attachment;filename=" + file.url}
    )
