# 建立資料表欄位
from main import db
from flask import current_app
#login
from flask_login import UserMixin,LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_no):
    return User.query.get(int(user_no))

class Permission:
    User = 1
    Monitor = 2
    Modify = 4
    Write = 8
    Delete = 16
    Admin = 32
    
#login user
class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'schema':'gpk'}
    no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False,index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __init__(self, **kwargs):
        super(Role,self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions +=perm
        
    def remove_permission(self,perm):
        if self.has_permission(perm):
            self.permissions -=perm

    def reset_permissions(self):
        self.permissions = 0
    
    def has_permission(self,perm):
        return self.permissions & perm ==perm

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.User],
            'Monitor': [Permission.User,Permission.Monitor],
            'Moderator': [Permission.User,Permission.Monitor,
                            Permission.Modify,Permission.Write],
            'Administrator': [Permission.User, Permission.Monitor,
                                Permission.Modify,Permission.Write, Permission.Delete,
                                Permission.Admin],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

class User(UserMixin,db.Model):
    __tablename__= 'users'
    __table_args__ = {'schema':'gpk'}
    no = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),unique=True)
    username = db.Column(db.String(64),unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    role_no = db.Column(db.Integer, db.ForeignKey('gpk.roles.no'))

    @property
    def id(self):
        return self.no
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        #return check_password_hash(self.password_hash, password)
        ##使用strip()使資料庫中的password欄位因固定長度的資料型態導致多餘的空白可以去除
        return check_password_hash(self.password_hash.strip(), password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # 使用者角色
    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     if self.role is None:
    #         if self.email == current_app.config['FLASKY_ADMIN']:
    #             self.role = Role.query.filter_by(name='Administrator').first()
    #         if self.role is None:
    #             self.role = Role.query.filter_by(default=True).first()
    # 使用者角色
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    # 使用者角色
    def is_administrator(self):
        return self.can(Permission.Admin)

    def __repr__(self):
        return '<User %r>' % self.username

# 使用者角色
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


#讀取資料庫資料的物件
class idc_name(db.Model):
    __tablename__= 'idc_table'
    __table_args__ = {'schema':'gpk'}

    idc_name = db.Column(db.String(10),primary_key=True)
    site = db.Column(db.String(10))
    #  設置關聯，relationship設置於一對多的『一』
    re_idc_name = db.relationship('s_name',backref='idcname',lazy="dynamic")
    def __repr__(self):
        return self.idc_name

class s_name(db.Model):
    __tablename__= 'server_table'
    __table_args__ = {'schema':'gpk'}
    server_name = db.Column(db.String(50),primary_key=True)
    #  設置外來鍵，ForeignKey設置於一對多的『多』
    idc_name = db.Column(db.String(10),db.ForeignKey('gpk.idc_table.idc_name'))
    bk_server_name = db.relationship('vs_name',backref='servername',lazy='dynamic')
    def __repr__(self):
        return self.server_name

class vs_name(db.Model):
    __tablename__= 'vserver_table'
    __table_args__ = {'schema':'gpk'}
    server_name = db.Column(db.String(50),db.ForeignKey('gpk.server_table.server_name'))
    vserver_name = db.Column(db.String(50),primary_key=True)
    #  設置關聯，relationship設置於一對多的『一』
    re_vservername = db.relationship('vs_soft',backref='vservername',lazy="dynamic")

    re_vservername = db.relationship('network',backref='vservername',lazy="dynamic")
    def __repr__(self):
        #return 'vServer # %r' % self.vserver_name
        return self.vserver_name

class vs_soft(db.Model):
    __tablename__= 'softservice_table'
    __table_args__ = {'schema':'gpk'}
    no = db.Column(db.Integer,primary_key=True)
    #  設置關聯，relationship設置於一對多的『一』
    re_no = db.relationship('webname',backref='softno',lazy="dynamic")
    #  設置外來鍵，ForeignKey設置於一對多的『多』
    vserver_name = db.Column(db.String(50),db.ForeignKey('gpk.vserver_table.vserver_name'))
    softservice_name = db.Column(db.String(20))
    status = db.Column(db.Boolean)
    #def __init__(self,softservice_name,vserver_name):
    #    self.softservice_name = softservice_name
    #    self.vserver_name = vserver_name
    def __repr__(self):
        #return self.softservice_name
        return self.vserver_name

class network(db.Model):
    __tablename__= 'network_table'
    __table_args__ = {'schema':'gpk'}
    #  設置外來鍵，ForeignKey設置於一對多的『多』
    vserver_name = db.Column(db.String(50),db.ForeignKey('gpk.vserver_table.vserver_name'))
    ipaddress = db.Column(db.String(20),primary_key=True)

    def __repr__(self):
        return self.vserver_name

class webname(db.Model):
    __tablename__= 'web_table'
    __table_args__ = {'schema':'gpk'}
    no = db.Column(db.Integer,primary_key=True)
    web_name = db.Column(db.String(30))
    #web_status = db.Column(db.Boolean)
    web_type = db.Column(db.String(20),db.ForeignKey('gpk.webtype_table.web_type'))
    softservice_no = db.Column(db.String(20),db.ForeignKey('gpk.softservice_table.no'))
    web_group = db.Column(db.String(20),db.ForeignKey('gpk.web_group.web_group'))
    revserver_name = db.Column(db.String(20),db.ForeignKey('gpk.rev_server.revserver_name'))
    note = db.Column(db.String(30))
    def __repr__(self):
        return self.web_name

class web_type(db.Model):
    __tablename__= 'webtype_table'
    __table_args__ = {'schema':'gpk'}
    no = db.Column(db.Integer)
    web_type = db.Column(db.String(20),primary_key=True)
    #  設置關聯，relationship設置於一對多的『一』
    re_webtype = db.relationship('webname',backref='webtype',lazy="dynamic")
    def __repr__(self):
        return self.web_type

        
class web_group(db.Model):
    __tablename__= 'web_group'
    __table_args__ = {'schema':'gpk'}
    web_group_id = db.Column(db.Integer)
    web_group = db.Column(db.String(20),primary_key=True)
    #  設置關聯，relationship設置於一對多的『一』
    re_webgroup = db.relationship('webname',backref='webgroup',lazy="dynamic")
    def __repr__(self):
        return self.web_group

        
class rev_server(db.Model):
    __tablename__= 'rev_server'
    __table_args__ = {'schema':'gpk'}
    revserver_id = db.Column(db.Integer)
    revserver_name = db.Column(db.String(20),primary_key=True)
    ipaddress_pub = db.Column(db.String(20))
    ipaddress_pri = db.Column(db.String(20))
    #  設置關聯，relationship設置於一對多的『一』
    re_revservername = db.relationship('webname',backref='revservername',lazy="dynamic")
    def __repr__(self):
        return self.revserver_name