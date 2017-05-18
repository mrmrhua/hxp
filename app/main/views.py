from flask import render_template,request,session,redirect,url_for,flash
from . import main
from app.common import get_access_token,get_user_info,get_wx_head
from app.model import User,db
from functools import wraps
from config import APPLYSTATUS,SEX,qiniu_access_key,qiniu_secret_key
from flask_login import login_user,login_required,current_user
from app import lm
from qiniu import Auth,urlsafe_base64_encode
import requests

lm.login_view = 'main.login'

@main.route('/')
def index():
    return  render_template('main/index.html')

@main.route('/index')
def toindex():
        return redirect(url_for('main.index'))

@main.route('/login')
def login():
    # 出二维码
    # state = request.args.get('state')
    # print(state)
    # if state is None:
    #     redirect('main/index.html')

    if not current_user.is_authenticated:  #未登录,去扫个码
        callback_url = 'http://127.0.0.1%3a5000/auth'
        re_url = 'https://open.weixin.qq.com/connect/qrconnect?appid=wxbfacdb1b99885182&redirect_uri=' + callback_url + '&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect'
        return redirect(re_url)  #扫完码会跳转到/auth
    if current_user.applystatus == APPLYSTATUS['PASS']:  #已登录,并且审核通过了,直接去个人中心
        return  redirect(url_for('.admin'))
    return redirect(url_for('.apply'))  #去填表

@main.route('/auth')
def auth():
    if 'code' not in request.args:
        # return render_template('tem.html')
        return "error"

    code = request.args.get('code')
    # if (request.args.get('state') != session['_csrf_token']):  # csrf
    #     return 'error'
    #     # 此处应该禁止操作 ?????????????????????????????????????????????

    result = get_access_token(code)

    if  result is None:   #return 404
        return "error"

    userinfo = get_user_info(result.get('access_token'),result.get('openid'))

    nickname = userinfo['nickname']
    unionid = userinfo['unionid']
    sex = userinfo['sex']
    headimg = userinfo['headimgurl']

    # 用户更换头像会导致微信的头像URL失效,因此要先存七牛
    r = get_wx_head(headimg)
    if(r==0):  #抓取不成功
        return redirect(url_for('main.index'))
    headimg = unionid+'.jpg'
    #存头像结束


    session['unionid'] = unionid

    # 根据unionid是否在库,决定是去填表还是去个人中心
    user = User.query.filter_by(unionid=unionid).first()
    if user is None:  # 第一次登陆
        applystatus = APPLYSTATUS['APPLYING']
        user = User(nickname=nickname, unionid=unionid, sex=sex, headimg=headimg, applystatus=applystatus)
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=True)
    session['applystatus'] = user.applystatus
    if user.applystatus==APPLYSTATUS['PASS']:  #已审核
        # 更新一下个人资料
        return url_for('.admin')   #去个人中心

    if user.applystatus == APPLYSTATUS['NOTPASS']:
        return redirect(url_for('.reapply'))

    #在提交过程中/或已提交在审核中
        #留前端处理

    return redirect(url_for('.apply'))

# 如果在申请状态,跳到applyform,
# 如果申请通过,跳到个人中心
# def is_applying():
#     if current_user.is_authenticated():
#         if current_user.applystatus == APPLYSTATUS['PASS']:
#             return   url_for('.admin')
#         return url_for('.apply')
#     return url_for('/login')

#
# # 只有在申请状态才能进入表单
# def is_applying(func):
#     @wraps(func)
#     def decorated_function(*args, **kwargs):
#         #     查看申请状态
#         #
#         if current_user.is_authenticated()==True:
#             if current_user.applystatus == APPLYSTATUS['PASS']:
#                 return func(*args, **kwargs)
#             return redirect(url_for('.apply'))
#         return redirect(url_for('/login'))
#     # return func(*args, **kwargs)
#
#     return decorated_function




@main.route('/apply')
@login_required  #补充:只有在审核的才能进
def apply():
    return render_template('main/baseform.html',applystatus=current_user.applystatus)


# def is_applying(func):
#     @wraps(func)
#     def decorated_function(*args, **kwargs):
#         if current_user.applystatus == APPLYSTATUS['PASS']:
#             return func(*args, **kwargs)
#
#     return decorated_function

@main.route('/admin')
@login_required
# @is_applying
def admin():  #补充:只有审核完成的才能进
    return "hello designers"


@main.route('/applyfail')
@login_required
def reapply():
    flash('抱歉,您的申请未通过审核.请填写完善信息后重新提交.')
    # 提示未通过
    current_user.applystatus = APPLYSTATUS['APPLYING']
    session['applystatus'] = current_user.applystatus
    db.session.add(current_user)
    db.session.commit()
    # 状态转为申请中
    return  redirect(url_for('.apply'))
    # 自动跳转申请页