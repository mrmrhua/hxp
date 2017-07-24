
from  flask import  request,jsonify,current_app,session
from flask_restful import Resource
from app.model import Applyform,Category,Applywork
from app import db,mail
from app.common import send_email
import json
from flask_login import current_user
from config import APPLYSTATUS


class Applyinfo(Resource):
    def post(self):
        c = json.loads(request.form.get('category'))
        imgurl = json.loads(request.form.get('img_url'))
        # 通知
        name = request.form.get('name')
        af = Applyform.from_request(request)
        send_email('mrmrhua@126.com', '新的入驻申请', body=name)
        # 修改状态
        current_user.applystatus = APPLYSTATUS['CHECKING']
        session['applystatus'] = current_user.applystatus
        db.session.add(current_user)
        db.session.add(af)
        db.session.commit()
        for t in c:
            c = Category(category_name=t,apply_id=af.id)
            db.session.add(c)
        for w in imgurl:
            aw = Applywork(work_url=w,apply_id=af.id)
            db.session.add(aw)
        db.session.commit()
        current_app.logger.info('新入驻设计师:%s' % af.name)
        return jsonify({'code':0})
