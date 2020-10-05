from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('記住我')
    submit = SubmitField('登入')

class RegistrationForm(FlaskForm):
    #username = StringField('Username', validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters,numbers,dots or''underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    #password = PasswordField('Password', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Passwords must match.')])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ServerAdd(FlaskForm):
    #Server = SelectField('ServerName',choices=[('gpk17_v01','gpk17_v01'),('gpk17_v02','gpk17_v02')])
    Server0 = StringField('Server Name  ( ex: gpk17_vh01 )')
    idcSelect0 = SelectField('IDC Name',choices=[])
    IPaddress0 = StringField('IP Address  ( ex: 10.22.1.1 )')
    #
    ServerSelect1 = SelectField('Server Name',choices=[])
    VServer1 = StringField('VServer Name  ( ex: systemlog1 )')
    IPaddress1 = StringField('IP Address  ( ex: 10.22.1.1 )')
    #
    ServerSelect2 = SelectField('Server Name',choices=[(0,'Please Select...')])
    VServerSelect2 = SelectField('VServer Name',choices=[(0,'Please Select Server First...')])

    Service2 = StringField('Service', [validators.Length(min=4, max=25)])
    #
    Web3 = StringField('Web Name',[validators.Required("Please enter Web URL.")])
    ServerWebtype3 = SelectField('Web Type',choices=[(0,'Please Select...')])
    ServerSelect3 = SelectField('Server Name',choices=[(0,'Please Select...')])
    VServerSelect3 = SelectField('VServer Name',choices=[(0,'Please Select Server First...')])
    ServiceSelect3 = SelectField('Service',choices=[(0,'Please Select VServer First ...')])
    Note3 = StringField('備註 ( 選填 )', [validators.required(), validators.length(max=10)])

class ServerModify(FlaskForm):
    ModifyServer0 = SelectField('實體主機',choices=[])
    Modifyidc0 = SelectField('IDC位置',choices=[])
    ModifyServer1 = SelectField('實體主機',choices=[])
    ModifyVServer1 = SelectField('虛擬主機',choices=[(0,'Please Select Server...')])
    ModifyIPaddress1 = SelectField('IP位置',choices=[(0,'Please Select VServer...')])
    ModifyServer2 = SelectField('虛擬主機',choices=[(0,'Please Select...')])
    ModifyVServer2 = SelectField('虛擬主機',choices=[(0,'Please Select Server First...')])
    ModifyService2 = SelectField('服務名稱',choices=[(0,'Please Select VServer First...')])
    ModifyWeb3 = SelectField('網站名稱',choices=[(0,'Please Select...')])
    
    #ModifyWeb = StringField('Web Name',[validators.Required("Please enter Web URL.")])
    #Modifywebtype = Col('Web Type')
    #ModifyServer = SelectField('Server Name')
    #ModifyVServer = SelectField('VServer Name')
    #ModifyService = Col('Service')

class SNameForm(FlaskForm):
    SelectIDC = SelectField('IDC',choices=[(0,'Please Select...'),('KSJNET','KSJNET'),('TCJNET','TCJNET')])
    SelectServer = SelectField('Server',choices=[])