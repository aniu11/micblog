# coding: utf-8
from datetime import datetime
from app import app, lm,db
from models import User, Post, ROLE_USER, ROLE_ADMIN
from flask import render_template, flash, redirect, session, url_for, g, request
from forms import LoginForm, SignUpForm, AboutMeForm, PublishBlogForm
from flask_login import current_user, login_required, login_user, logout_user
from utils import PER_PAGE


@app.route('/')
@app.route('/index')
def index():
    # app.logger.debug(current_user.is_authenticated())
    # app.logger.debug(current_user.is_anonymous())
    user = {'nickname': 'Miguel'}  # 用户名
    posts = [  # 提交内容
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 此处的current_user 为 User 类型
    if current_user.is_authenticated():
        return redirect('index')

    # 表单验证
    form = LoginForm()
    # 动作处理
    if form.validate_on_submit():
        user = User.login_check(request.form.get('user_name'))
        if user:
            login_user(user)
            user.last_seen = datetime.now()

            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash('Database Err')
                return redirect('/login')
            flash('Your name: ' + request.form.get('user_name'))
            flash('remember me? ' + str(request.form.get('remember_me')))
            return redirect(url_for('users', user_id=current_user.id))
        else:
            flash('Login Failed, name not exist')
            return redirect('/login')
    app.logger.debug(form.errors)
    return render_template('login.html', title='Sign In', form=form)


@lm.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've logged out")
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    user = User()
    if form.validate_on_submit():
        user_name = request.form.get('user_name')
        user_email = request.form.get('user_email')
        password = request.form.get('password')

        check = User.query.filter(db.or_(
            User.nickname == user_name, User.email == user_email)).first()
        if check:
            flash('Already Exist')
            return redirect('/signup')

        if len(user_name) and len(user_email):
            user.nickname = user_name
            user.email = user_email
            user.role = ROLE_USER
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash('DB Err')
                return redirect('signup')

            flash('Signup Success')
            return redirect('/index')
    return render_template('signup.html', form=form)


@app.route('/user/<int:user_id>', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/user/<int:user_id>/page/<int:page>', methods=['GET', 'POST'])
@login_required
def users(user_id, page):
    form = AboutMeForm()
    if user_id != current_user.id:
        flash('You can only visit your own profile')
        return redirect(url_for('index'))

    user = User.query.filter(User.id == user_id).first()
    if not user:
        flash('user not exist')
        return redirect('/index')

    # blogs = user.paginate(page, PER_PAGE, False).items
    pagination = Post.query.filter(user_id == current_user.id)\
        .order_by(db.desc(Post.timestamp)).paginate(page, PER_PAGE, False)
    return render_template('user.html', form=form, user=user, pagination=pagination)


@app.route('/publish/<int:user_id>', methods=['GET', 'POST'])
@login_required
def publish(user_id):
    form = PublishBlogForm()
    posts = Post()
    if form.validate_on_submit():
        content = request.form.get('body')
        if not len(str(content).strip()):
            flash('content required !')
            return redirect(url_for('publish', user_id=user_id))
        posts.body = content
        posts.timestamp = datetime.now()
        posts.user_id = user_id

        try:
            db.session.add(posts)
            db.session.commit()
        except:
            flash('DB Err')
            return redirect(url_for('publish', user_id=user_id))

    return render_template('publish.html', form=form)


@app.route('/about-me/<int:user_id>', methods=['POST'])
@login_required
def about_me(user_id):
    user = User.query.filter(User.id == user_id).first()
    if request.method == 'POST':
        content = request.form.get('describe')
        if len(content) and len(content) < 140:
            user.about_me = content
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash('DB Err')
                return redirect(url_for('users', user_id=user_id))
        else:
            flash('maybe something wrong with your input')
    return redirect(url_for('users', user_id=user_id))
