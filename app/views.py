# coding: utf-8
from datetime import datetime
from app import app, lm,db
from models import User, ROLE_USER, ROLE_ADMIN
from flask import render_template, flash, redirect, session, url_for, g, request
from forms import LoginForm, SignUpForm, AboutMeForm
from flask_login import current_user, login_required, login_user, logout_user


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


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def users(user_id):
    form = AboutMeForm()
    user = User.query.filter(User.id == user_id).first()
    if not user:
        flash('user not exist')
        return redirect('/index')
    blogs = user.posts.all()
    return render_template('user.html', form=form, user=user, blogs=blogs)

