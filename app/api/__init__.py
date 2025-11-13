from flask_restful import Api
from .resource import SubjectListResource, SubjectResource

api = Api(prefix = '/api')
# Register resources
api.add_resource(SubjectListResource, '/subjects')
api.add_resource(SubjectResource, '/subjects/<int:subject_id>')