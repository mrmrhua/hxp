import urllib
import  json
from flask_mail import Message
from app import mail
import requests
from qiniu import Auth,urlsafe_base64_encode
import requests
from config import qiniu_secret_key,qiniu_access_key

def get_access_token(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxbfacdb1b99885182&secret=c4f876b16ddc8d8e4259b9c2388e5493&code='\
              + code + '&grant_type=authorization_code'

    # get acess_token
    result = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))

    if('errcode' in result.keys()):
        return  None
    # 此处 应该提示登录失败 ?????????????????????????????????????????????

    access_token = result['access_token']
    openid = result['openid']

    return  {'access_token':access_token,'openid':openid}



def get_user_info(access_token,openid):
    # get user info
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token={a}&openid={b}'.format(a=access_token,b=openid)
    userinfo = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))

    # nickname = userinfo['nickname']
    # unionid = userinfo['unionid']
    # sex = userinfo['sex']
    # headimg = userinfo['headimgurl']

    return userinfo


def send_email(to,subject,body):
    # msg = Message(subject='猴小胖网站通知:'+subject,sender='houxiaopangdeisgn@163.com',recipients=[to])
    # msg.body = body
    # mail.send(msg)

    url = "http://api.sendcloud.net/apiv2/mail/send"

    # 您需要登录SendCloud创建API_USER，使用API_USER和API_KEY才可以进行邮件的发送。
    params = {"apiUser": "hxp_devmail", \
              "apiKey": "6CEiNLCT8Q8UfSug", \
              "from": "dev@devmail.houxiaopang.com", \
              "fromName": "devmail", \
              "to": to, \
              "subject": "猴小胖网站通知"+subject, \
              "html": body, \
              }

    r = requests.post(url, files={}, data=params)
    print(r.text)


def get_wx_head(headimg):
    Encodedurl = urlsafe_base64_encode(headimg)
    Encodedentryuri = urlsafe_base64_encode('userhead:' + unionid + ".jpg")
    upheadurl = '/fetch/' + Encodedurl + '/to/' + Encodedentryuri
    Host = 'iovip.qbox.me'
    Content_type = 'application/x-www-form-urlencoded'
    requrl = "http://" + Host + upheadurl

    q = Auth(qiniu_access_key, qiniu_secret_key)
    AccessToken = q.token_of_request(requrl, content_type=Content_type)

    Authorization = 'QBox ' + AccessToken
    headers = {'Host': Host,
               'Content-Type': Content_type,
               'Authorization': Authorization,
               }
    r = requests.post(requrl, headers=headers)
    if (r.status_code != 200):  # 抓取不成功
        return 0
    else:
        return 1



