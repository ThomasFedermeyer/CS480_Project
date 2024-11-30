from flask import Flask
from flask_cors import CORS

from db import DB_CONFIG
from admin.developer_type import developer_type_bp
from admin.technology_type import technology_type_bp
from admin.tools import tool_bp
from admin.resource import resource_bp
from admin.company import company_bp
from admin.user import user_bp
from admin.technology import technology_bp
from admin.project import project_bp
from admin.assign_user_project import assigned_to_bp
from admin.learns_user_resource import learns_from_bp
from admin.uses_project_technology import project_uses_technology_bp
from admin.resource_teaches_technology import resource_teaches_technology_bp
from admin.resource_uses_tool import resource_uses_tool_bp
from admin.technology_dependency import technology_dependency_bp
from admin.developer_position import developer_position_bp

from developer_profile import developer_profile_bp
from popular_technologies import popular_technologies_bp
from employment import employment_bp
import pymysql

app = Flask(__name__)
app.register_blueprint(developer_type_bp, url_prefix='/api/admin/developerTypes')
app.register_blueprint(technology_type_bp, url_prefix='/api/admin/technologyTypes')
app.register_blueprint(tool_bp, url_prefix='/api/admin/tools')
app.register_blueprint(resource_bp, url_prefix='/api/admin/resources')
app.register_blueprint(company_bp, url_prefix='/api/admin/companies')
app.register_blueprint(user_bp, url_prefix='/api/admin/users')
app.register_blueprint(technology_bp, url_prefix='/api/admin/technologies')
app.register_blueprint(project_bp, url_prefix='/api/admin/projects')
# relations
app.register_blueprint(assigned_to_bp, url_prefix='/api/admin/assignments')
app.register_blueprint(learns_from_bp, url_prefix='/api/admin/learns_from')
app.register_blueprint(project_uses_technology_bp, url_prefix='/api/admin/project_uses_technology')
app.register_blueprint(resource_teaches_technology_bp, url_prefix='/api/admin/resource_teaches_technology')
app.register_blueprint(resource_uses_tool_bp, url_prefix='/api/admin/resource_uses_tool')
app.register_blueprint(technology_dependency_bp, url_prefix='/api/admin/technology_dependency')
app.register_blueprint(developer_position_bp, url_prefix='/api/admin/developer_positions')

# developer profile
app.register_blueprint(developer_profile_bp, url_prefix='/api/developer_profile')
# popular technologies
app.register_blueprint(popular_technologies_bp, url_prefix='/api/popular_technologies')
# employment
app.register_blueprint(employment_bp, url_prefix='/api/employment')

CORS(app)


app.config['MYSQL_HOST'] = DB_CONFIG['host']
app.config['MYSQL_USER'] = DB_CONFIG['user']
app.config['MYSQL_PASSWORD'] = DB_CONFIG['password']
app.config['MYSQL_DB'] = DB_CONFIG['database']

@app.route('/')
def admin_main():
    return 'Your Flask Server Running'
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)
