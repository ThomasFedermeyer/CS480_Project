from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

developer_position_bp = Blueprint('developer_position', __name__)
PER_PAGE = 10

@developer_position_bp.route('/', methods=['GET'])
def get_positions():
    allowed_params = ['page', 'sort', 'sortBy', 'userName', 'developerTypeName', 'companyName', 'remotePolicy', 'minSalary', 'maxSalary', 'workingTime']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='UserID', type=str)
    userNameMatch = request.args.get('userName', default='', type=str)
    developerTypeNameMatch = request.args.get('developerTypeName', default='', type=str)
    companyName = request.args.get('companyName', default=None, type=str)
    remotePolicy = request.args.get('remotePolicy', default=None, type=str)
    minSalary = request.args.get('minSalary', default=None, type=int)
    maxSalary = request.args.get('maxSalary', default=None, type=int)
    workingTime = request.args.get('workingTime', default=None, type=int)

    companyQuery = 'AND Company.Name = \'{}\''.format(companyName) if companyName else ''
    remotePolicyQuery = 'AND RemotePolicy = \'{}\''.format(remotePolicy) if remotePolicy else ''
    minSalaryQuery = 'AND Salary >= {}'.format(minSalary) if minSalary else ''
    maxSalaryQuery = 'AND Salary <= {}'.format(maxSalary) if maxSalary else ''
    workingTimeQuery = 'AND WorkingTime = {}'.format(workingTime) if workingTime else ''

    valid_sort_by = ['UserID' , 'UserName', 'Salary']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['position']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT Position.DeveloperTypeID AS DeveloperTypeID, DeveloperType.Name AS DeveloperTypeName, Position.UserID AS UserID, User.Name AS UserName, Position.CompanyID AS CompanyID, Company.Name AS CompanyName, RemotePolicy, Salary, WorkingTime
                    FROM {} JOIN {} ON {}.DeveloperTypeID = {}.TypeID JOIN {} ON {}.UserID = {}.UserID JOIN {} ON {}.CompanyID = {}.CompanyID
                    WHERE User.Name LIKE \'{}\' AND
                    DeveloperType.Name LIKE \'{}\'
                    {} {} {} {} {}
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['position'], DB_TABLES['developer_type'], DB_TABLES['position'], DB_TABLES['developer_type'], DB_TABLES['user'], DB_TABLES['position'], DB_TABLES['user'], DB_TABLES['company'], DB_TABLES['position'], DB_TABLES['company'],
                                userNameMatch + '%', developerTypeNameMatch + '%', companyQuery, remotePolicyQuery, minSalaryQuery, maxSalaryQuery, workingTimeQuery, sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                res_data = []
                for item in data:
                    res_data.append({
                        'developerTypeID': item['DeveloperTypeID'],
                        'developerTypeName': item['DeveloperTypeName'],
                        'userID': item['UserID'],
                        'userName': item['UserName'],
                        'companyID': item['CompanyID'],
                        'companyName': item['CompanyName'],
                        'remotePolicy': item['RemotePolicy'],
                        'salary': item['Salary'],
                        'workingTime': item['WorkingTime']
                    })
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Positions Fetched Successfully', 'data': res_data }), 200



@developer_position_bp.route('/addPositions', methods=['POST'])
def insert_positions():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    positions = request.get_json()
    
    if 'positions' not in positions:
        return jsonify({'error': 'Incorrect Body: Could not find positions'}), 400
    
    values_to_insert = []
    for position in positions['positions']:
        developerTypeId = position.get('developerTypeId')
        userId = position.get('userId')
        companyId = position.get('companyId')
        remotePolicy = position.get('remotePolicy')
        salary = position.get('salary')
        workingTime = position.get('workingTime')
        
        if not developerTypeId or not userId or not companyId:
            return jsonify({'error': 'Each position must have a developerTypeId and userId and companyId'}), 400
        
        values_to_insert.append((developerTypeId, userId, companyId, remotePolicy, salary, workingTime))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (DeveloperTypeID, UserID, CompanyID, RemotePolicy, Salary, WorkingTime)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """.format(DB_TABLES['position']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Positions Inserted Successfully'}), 201

@developer_position_bp.route('/updatePosition', methods=['PUT'])
def update_position():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    position_data = request.get_json()

    developerTypeId = position_data.get('developerTypeId')
    userId = position_data.get('userId')
    companyId = position_data.get('companyId')
    remotePolicy = position_data.get('remotePolicy')
    salary = position_data.get('salary')
    workingTime = position_data.get('workingTime')

    if not developerTypeId or not userId or not companyId:
        return jsonify({'error': 'Position must have a developerTypeID and userId and companyId'}), 400
    
    update_fields = []
    update_values = []

    if remotePolicy:
        update_fields.append("RemotePolicy = %s")
        update_values.append(remotePolicy)
    
    if salary:
        update_fields.append("Salary = %s")
        update_values.append(salary)
    
    if workingTime:
        update_fields.append("WorkingTime = %s")
        update_values.append(workingTime)
    
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    
    update_values.append(developerTypeId)
    update_values.append(userId)
    update_values.append(companyId)

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    UPDATE {} SET {}
                    WHERE DeveloperTypeID = %s AND UserID = %s AND CompanyID = %s
                """.format(DB_TABLES['position'], ', '.join(update_fields)), update_values)
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Position not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Position Updated Successfully'}), 200

@developer_position_bp.route('/deletePositionsByDeveloperTypeID', methods=['DELETE'])
def delete_positions_by_developer_type_id():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    developerTypeId = data.get('developerTypeId')
    
    if not developerTypeId:
        return jsonify({'error': 'developerTypeId must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE DeveloperTypeID = %s
                """.format(DB_TABLES['position']), (developerTypeId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Position(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Positions Deleted Successfully'}), 200

@developer_position_bp.route('/deletePositionsByUserID', methods=['DELETE'])
def delete_positions_by_user_id():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    userId = data.get('userId')
    
    if not userId:
        return jsonify({'error': 'userId must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE UserID = %s
                """.format(DB_TABLES['position']), (userId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Position(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Positions Deleted Successfully'}), 200

@developer_position_bp.route('/deletePositionsByCompanyID', methods=['DELETE'])
def delete_positions_by_company_id():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    companyId = data.get('companyId')
    
    if not companyId:
        return jsonify({'error': 'companyId must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE CompanyID = %s
                """.format(DB_TABLES['position']), (companyId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Position(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Positions Deleted Successfully'}), 200