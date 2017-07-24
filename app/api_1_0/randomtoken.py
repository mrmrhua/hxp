from  flask import  session,jsonify
import  random
from flask_restful import Resource
from flask_session import Session

# SESSION_TYPE='redis'

# 生成TOKEN(随机数)并存到session
def generate_csrf_token():
    # session.clear()
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(random.randint(0,199))
    return session['_csrf_token']

# token,re_url api
class RandomToken(Resource):
    def get(self):
        return  jsonify({'state':generate_csrf_token()})



