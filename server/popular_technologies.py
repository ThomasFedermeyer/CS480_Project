from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES
import pandas as pd

popular_technologies_bp = Blueprint('popular_technologies', __name__)
PER_PAGE = 10

# technologies
@popular_technologies_bp.route('/getTechnologies', methods=['GET'])
def get_technologies():
    allowed_params = ['page', 'sort', 'sortBy', 'name', 'fromDate', 'toDate', 'type']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='TechID', type=str)
    nameMatch = request.args.get('name', default='', type=str)
    fromDate = request.args.get('fromDate', default='', type=str)
    toDate = request.args.get('toDate', default='', type=str)
    technologyType = request.args.get('type', default='', type=str)

    fromDateQuery = 'AND DateOfRelease >= \'{}\''.format(fromDate) if fromDate else ''
    toDateQuery = 'AND DateOfRelease <= \'{}\''.format(toDate) if toDate else ''
    technologyTypeQuery = 'AND TechnologyType.Name = \'{}\''.format(technologyType) if technologyType else ''

    valid_sort_by = ['TechID', 'TechName', 'DateOfRelease']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['technology']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT Technology.TechID, Technology.Name AS TechName, DateOfRelease, Technology.TypeID, TechnologyType.Name as TypeName, Technology_UseCases.UseCase 
                    FROM {} JOIN {} ON {}.TypeID = {}.TypeID LEFT JOIN {} ON {}.TechID = {}.TechID
                    WHERE Technology.Name LIKE \'{}\'
                    {} {} {}
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['technology'], DB_TABLES['technology_type'], DB_TABLES['technology'], DB_TABLES['technology_type'], DB_TABLES['technology_use_case'], DB_TABLES['technology'], DB_TABLES['technology_use_case'],
                            nameMatch + '%', fromDateQuery, toDateQuery, technologyTypeQuery, sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                grouped_data = {}
                for item in data:
                    if item['TechID'] not in grouped_data:
                        grouped_data[item['TechID']] = {
                            'id': item['TechID'],
                            'name': item['TechName'],
                            'dateOfRelease': item['DateOfRelease'],
                            'type': item['TypeName'],
                            'useCases': ''
                        }
                    if item['UseCase']:
                        grouped_data[item['TechID']]['useCases'] += ' | ' + item['UseCase']
                
                res_data = list(grouped_data.values())
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Technologies Fetched Successfully', 'data': res_data, 'total_pages': total_pages }), 200

@popular_technologies_bp.route('/getResourcesPerTechnology', methods=['GET'])
def get_resources_per_technology():

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                query_string = """
                    SELECT Technology.Name AS TechName, Resource.Name AS ResourceName
                    FROM {} LEFT JOIN {} ON Technology.TechID = Resource_Teaches_Technology.TechID LEFT JOIN {} ON Resource_Teaches_Technology.ResourceID = Resource.ResourceID
                    """.format(DB_TABLES['technology'], DB_TABLES['resource_teaches_technology'], DB_TABLES['resource'])
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                df = pd.DataFrame(data, columns=['TechName', 'ResourceName'])
                # group by tech name so that the resource names are gruped in a list
                grouped_data = df.groupby('TechName')['ResourceName'].apply(lambda x: [name for name in x if name]).reset_index(name='ResourceNames')
                res_data = grouped_data.to_dict(orient='records')
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500

    return jsonify({ 'error': False, 'message': 'Resources Fetched Successfully', 'data': res_data }), 200

@popular_technologies_bp.route('/getUsersAndDeveloperTypesPerTechnology', methods=['GET'])
def get_users_and_developer_types_per_technology():
    allowed_params = ['developerTypeName']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    developerTypeNameFilter = request.args.get('developerTypeName', default=None, type=str)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                query_string = """
                    SELECT 
                        Technology.Name AS TechName,
                        Assigned_To.UserID,
                        DeveloperType.Name AS DeveloperTypeName
                    FROM 
                        {} AS Technology
                    LEFT JOIN 
                        {} AS Project_Uses_Technology ON Technology.TechID = Project_Uses_Technology.TechID
                    LEFT JOIN 
                        {} AS Assigned_To ON Project_Uses_Technology.ProjectID = Assigned_To.ProjectID
                    LEFT JOIN 
                        {} AS User ON Assigned_To.UserID = User.UserID
                    LEFT JOIN 
                        {} AS Position ON User.UserID = Position.UserID
                    LEFT JOIN 
                        {} AS DeveloperType ON Position.DeveloperTypeID = DeveloperType.TypeID
                    """.format(DB_TABLES['technology'], DB_TABLES['project_uses_technology'], DB_TABLES['assigned_to'], DB_TABLES['user'], DB_TABLES['position'], DB_TABLES['developer_type'])
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                df = pd.DataFrame(data, columns=['TechName', 'UserID', 'DeveloperTypeName'])

                all_technologies = pd.DataFrame({'TechName': df['TechName'].unique()})

                if developerTypeNameFilter:
                    df = df[df['DeveloperTypeName'] == developerTypeNameFilter]
                
                grouped_data = df.groupby('TechName')['UserID'].count().reset_index(name='counts')
                
                
                grouped_data = all_technologies.merge(grouped_data, on='TechName', how='left').fillna(0)
                grouped_data['counts'] = grouped_data['counts'].astype(int)
                
                res_data = grouped_data.to_dict(orient='records')
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500

    return jsonify({ 'error': False, 'message': 'Data Fetched Successfully', 'data': res_data }), 200

#tools
@popular_technologies_bp.route('/getTools', methods=['GET'])
def get_tools():
    allowed_params = ['page', 'sort', 'sortBy', 'name', 'type', 'sync', 'fromDate', 'toDate']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='ToolID', type=str)
    nameMatch = request.args.get('name', default='', type=str)
    toolType = request.args.get('type', default='', type=str)
    sync = request.args.get('sync', default=None, type=str)
    fromDate = request.args.get('fromDate', default='', type=str)
    toDate = request.args.get('toDate', default='', type=str)

    toolTypeQuery = 'AND Type = \'{}\''.format(toolType) if toolType else ''
    syncQuery = 'AND SyncCapability = \'{}\''.format(sync) if sync else ''
    fromDateQuery = 'AND DateOfRelease >= \'{}\''.format(fromDate) if fromDate else ''
    toDateQuery = 'AND DateOfRelease <= \'{}\''.format(toDate) if toDate else ''

    valid_sort_by = ['ToolID', 'Name', 'DateOfRelease']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['tool']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT * FROM {} NATURAL LEFT JOIN {} WHERE Name LIKE \'{}\'
                    {} {} {} {}
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['tool'], DB_TABLES['tool_primary_purpose'],
                         nameMatch + '%', toolTypeQuery, syncQuery, fromDateQuery, toDateQuery, sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                grouped_data = {}
                for item in data:
                    if item['ToolID'] not in grouped_data:
                        grouped_data[item['ToolID']] = {
                            'id': item['ToolID'],
                            'name': item['Name'],
                            'type': item['Type'],
                            'sync': item['SyncCapability'],
                            'dateOfRelease': item['DateOfRelease'],
                            'primaryPurposes': ''
                        }
                    if item['PrimaryPurpose']:
                        grouped_data[item['ToolID']]['primaryPurposes'] += ' | ' + item['PrimaryPurpose']
                
                res_data = list(grouped_data.values())
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Tools Fetched Successfully', 'data': res_data, 'total_pages': total_pages }), 200

@popular_technologies_bp.route('/getResourcesPerTool', methods=['GET'])
def get_resources_per_tool():

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                query_string = """
                    SELECT Tool.Name AS ToolName, Resource.Name AS ResourceName
                    FROM {} LEFT JOIN {} ON Tool.ToolID = Resource_Uses_Tool.ToolID LEFT JOIN {} ON Resource_Uses_Tool.ResourceID = Resource.ResourceID
                    """.format(DB_TABLES['tool'], DB_TABLES['resource_uses_tool'], DB_TABLES['resource'])
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                df = pd.DataFrame(data, columns=['ToolName', 'ResourceName'])
                # group by tool name so that the resource names are gruped in a list
                grouped_data = df.groupby('ToolName')['ResourceName'].apply(lambda x: [name for name in x if name]).reset_index(name='ResourceNames')
                res_data = grouped_data.to_dict(orient='records')
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500

    return jsonify({ 'error': False, 'message': 'Resources Fetched Successfully', 'data': res_data }), 200

