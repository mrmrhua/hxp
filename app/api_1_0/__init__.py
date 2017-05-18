from flask import Blueprint
from flask_restful import Api,Resource
from app.exceptions import ValidationError


api_bp = Blueprint('api',__name__)
api = Api(api_bp)

# Import apis in the package
from .randomtoken import RandomToken
from .admin_project import AddProject
from  .milestone import GetMilestone
from  .qiniu_uptoken import GetUpToken
from  .upwork import UpWork
from .getwork import GetWork
from .getdetail import GetDetail
from .applyuptoken import GetApplyUptoken
from .applyform import   Applyinfo
from .applystatus import GetApplyStatus
# add apis to specific uris
api.add_resource(RandomToken,'/randomtoken')

api.add_resource(AddProject,'/admin/project')

api.add_resource(GetMilestone,'/project/milestone')

api.add_resource(GetUpToken,'/file/uptoken')

api.add_resource(UpWork,'/project/add_history_work')

api.add_resource(GetWork,'/project/milestone/work')

api.add_resource(GetDetail,'/project/workdetail/<int:id>')

api.add_resource(GetApplyUptoken,'/apply/uptoken')

api.add_resource(Applyinfo,'/apply/form')

api.add_resource(GetApplyStatus,'/apply/status')