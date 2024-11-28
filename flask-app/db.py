import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mehul160401',
    'database': 'developer_survey'
}

DB_TABLES = {
    'developer_type': 'DeveloperType',
    'technology_type': 'TechnologyType',
    'technology': 'Technology',
    'technology_use_case': 'Technology_UseCases',
    'tool': 'Tool',
    'tool_primary_purpose': 'Tool_PrimaryPurpose',
    'resource': 'Resource',
    'company': 'Company',
    'user': 'User',
    'project': 'Project',
    'assigned_to': 'Assigned_To',
    'learns_from': 'Learns_From',
    'project_uses_technology': 'Project_Uses_Technology',
    'resource_teaches_technology': 'Resource_Teaches_Technology',
    'resource_uses_tool': 'Resource_Uses_Tool',
    'technology_dependency': 'Technology_Dependency',
    'position': 'Position'
}

def get_db_connection():
    return pymysql.connect(
        host = DB_CONFIG['host'],
        user = DB_CONFIG['user'],
        password= DB_CONFIG['password'],
        db = DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor
    )
