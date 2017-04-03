# coding:utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(Form):
    """
    登录表单 包括用户名密码和是否记住
    """
    user_name = StringField('user_name', validators=[DataRequired(), Length(max=15)])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Login')


class SignUpForm(Form):
    """
    注册表单
    """
    user_email = StringField('user_email', validators=[DataRequired(), Email(), Length(max=128)])
    user_name = StringField('user_name', validators=[DataRequired(), Length(max=15)])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AboutMeForm(Form):
    """
    个人描述表单
    """
    describe = TextAreaField('about me', validators=[DataRequired(), Length(max=140)])
    submit = SubmitField('Yes')

