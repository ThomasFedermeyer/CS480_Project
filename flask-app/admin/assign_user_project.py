from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

assigned_to_bp = Blueprint('assigned_to', __name__)
PER_PAGE = 10

@assigned_to_bp.route('/', methods=['GET'])
def get_assignments():
    allowed_params = ['page', 'sort', 'sortBy', 'userName', 'projectName', 'role']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='UserID', type=str)
    userNameMatch = request.args.get('userName', default='', type=str)
    projectNameMatch = request.args.get('projectName', default='', type=str)
    role = request.args.get('role', default=None, type=str)

    roleQuery = 'AND Role = \'{}\''.format(role) if role else ''

    valid_sort_by = ['UserID' , 'UserName', 'ProjectName']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['assigned_to']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT Assigned_To.UserID AS UserID, User.Name AS UserName, Assigned_To.ProjectID AS ProjectID, Project.Name AS ProjectName, Role
                    FROM {} JOIN {} ON {}.UserID = {}.UserID JOIN {} ON {}.ProjectID = {}.ProjectID
                    WHERE User.Name LIKE \'{}\' AND
                    Project.Name LIKE \'{}\'
                    {}
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['assigned_to'], DB_TABLES['user'], DB_TABLES['assigned_to'], DB_TABLES['user'], DB_TABLES['project'], DB_TABLES['assigned_to'], DB_TABLES['project'],
                                userNameMatch + '%', projectNameMatch + '%', roleQuery, sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                res_data = []
                for item in data:
                    res_data.append({
                        'userID': item['UserID'],
                        'userName': item['UserName'],
                        'projectID': item['ProjectID'],
                        'projectName': item['ProjectName'],
                        'role': item['Role']
                    })
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Assignments Fetched Successfully', 'data': res_data }), 200



@assigned_to_bp.route('/addAssignments', methods=['POST'])
def insert_assignments():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    assignments = request.get_json()
    
    if 'assignments' not in assignments:
        return jsonify({'error': 'Incorrect Body: Could not find assignments'}), 400
    
    values_to_insert = []
    for assignment in assignments['assignments']:
        userId = assignment.get('userId')
        projectId = assignment.get('projectId')
        role = assignment.get('role')
        
        if not userId or not projectId:
            return jsonify({'error': 'Each assignment must have a userId or projectId'}), 400
        
        values_to_insert.append((userId, projectId, role))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (UserID, ProjectID, Role)
                    VALUES (%s, %s, %s)
                """.format(DB_TABLES['assigned_to']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Assignments Inserted Successfully'}), 201

@assigned_to_bp.route('/deleteAssignmentsByUserID', methods=['DELETE'])
def delete_assignments_by_user_id():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    userId = data.get('userId')
    
    if not userId:
        return jsonify({'error': 'UserID must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE UserID = %s
                """.format(DB_TABLES['assigned_to']), (userId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Assignment(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Assignments Deleted Successfully'}), 200

@assigned_to_bp.route('/deleteAssignmentsByProjectID', methods=['DELETE'])
def delete_assignments_by_project_id():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    projectId = data.get('projectId')
    
    if not projectId:
        return jsonify({'error': 'ProjectID must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE ProjectID = %s
                """.format(DB_TABLES['assigned_to']), (projectId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Assignment(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Assignments Deleted Successfully'}), 200