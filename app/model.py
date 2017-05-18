from flask_login import UserMixin,current_user
from app import lm,db
from flask import request,json
from config import APPLYSTATUS
from schema import Schema

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String(64))
    unionid = db.Column(db.String(64))
    applystatus = db.Column(db.Integer,default=APPLYSTATUS['APPLYING'])
    sex =  db.Column(db.Integer)
    headimg = db.Column(db.String(255))

    def __repr__(self):
        return '<User %r>' % self.nickname

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(6))
    description = db.Column(db.String(255))
    milestone_num = db.Column(db.Integer)
    # 可用Milestone.project来访问
    milestones = db.relationship('Milestone',backref='project')

    def __repr__(self):
        return '<Project %r>' % self.description

class Milestone(db.Model):
    __tablename__ = 'milestones'
    id = db.Column(db.Integer, primary_key=True)
    due_time = db.Column(db.DateTime)
    de_status = db.Column(db.Integer,default=0)
    cl_status = db.Column(db.Integer,default=0)
    pro_id = db.Column(db.Integer,db.ForeignKey('projects.id'))
    ordinpro = db.Column(db.Integer)
    due_time_cli = db.Column(db.DateTime)
    # 可用Historywork.milestone来访问
    historywork = db.relationship('Historywork',backref='milestone')

    def __repr__(self):
        return '<Milestone %r>' % self.due_time

class Historywork(db.Model):
    __tablename__ = 'historywork'
    id = db.Column(db.Integer, primary_key=True)
    work_url = db.Column(db.String(255))
    up_time = db.Column(db.DateTime)
    milestone_id = db.Column(db.Integer, db.ForeignKey('milestones.id'))

    def __repr__(self):
        return '<Historywork %r>' % self.work_url


class Applyform(db.Model):
    __tablename__ = 'applyforms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16),nullable=True)
    sex = db.Column(db.Integer,nullable=True)
    born = db.Column(db.Integer,nullable=True)
    tel = db.Column(db.String(11),nullable=True)
    email = db.Column(db.String(64),nullable=True)
    qq = db.Column(db.String(16) ,nullable=True)
    wx = db.Column(db.String(64) ,nullable=True)
    school = db.Column(db.String(64),nullable=True)
    major = db.Column(db.String(64),nullable=True)
    graduate = db.Column(db.Integer,nullable=True)
    project_text = db.Column(db.Text,nullable=True)
    blog_url = db.Column(db.String(255),nullable=True)
    worktime = db.Column(db.String(16), nullable=True)
    identity = db.Column(db.Integer,nullable=True)
    unionid = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)

    @staticmethod
    def  from_request(request):
        name = request.form.get('name')
        sex = request.form.get('sex')
        born = request.form.get('born')
        tel = request.form.get('tel')
        email = request.form.get('email')
        # may be none
        qq = request.form.get('qq')
        wx = request.form.get('wx')
        school = request.form.get('school')
        major = request.form.get('major')
        graduate = request.form.get('graduate')
        # may be none
        c = json.loads(request.form.get('category'))
        # 保留JSON字符串包装的数组形式
        worktime = request.form.get('worktime')
        identity = request.form.get('identity')
        # may be none
        project_text = request.form.get('project_text')
        blog_url = request.form.get('blog_url')
        imgurl = json.loads(request.form.get('img_url'))
        unionid = current_user.unionid

        return  Applyform(name=name,sex=int(sex),born=int(born),tel=int(tel),email=email,qq=qq,wx=wx,school=school,major=major,graduate=int(graduate),project_text=project_text,blog_url=blog_url,identity=identity,worktime=worktime,unionid=unionid)





    def __repr__(self):
        return '<Applyform %r>' % self.name

class Applywork(db.Model):
    __tablename__ = 'applyworks'
    id = db.Column(db.Integer,primary_key=True)
    work_url = db.Column(db.String(255))
    apply_id = db.Column(db.Integer,db.ForeignKey('applyforms.id'))

    def __repr__(self):
        return '<Applywork %r>' % self.work_url

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64))
    apply_id = db.Column(db.Integer, db.ForeignKey('applyforms.id'))

    def __repr__(self):
        return '<Category of %r>' % self.apply_id
