from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

learns_from_bp = Blueprint('learns_from', __name__)
PER_PAGE = 10

@learns_from_bp.route('/', methods=['GET'])
def get_records():
    allowed_params = ['page', 'sort', 'sortBy', 'userName', 'resourceName']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='UserID', type=str)
    userNameMatch = request.args.get('userName', default='', type=str)
    resourceNameMatch = request.args.get('resourceName', default='', type=str)

    valid_sort_by = ['UserID' , 'UserName', 'ResourceName']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['learns_from']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT Learns_From.UserID AS UserID, User.Name AS UserName, Learns_From.ResourceID AS ResourceID, Resource.Name AS ResourceName
                    FROM {} JOIN {} ON {}.UserID = {}.UserID JOIN {} ON {}.ResourceID = {}.ResourceID
                    WHERE User.Name LIKE \'{}\' AND
                    Resource.Name LIKE \'{}\' 
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['learns_from'], DB_TABLES['user'], DB_TABLES['learns_from'], DB_TABLES['user'], DB_TABLES['resource'], DB_TABLES['learns_from'], DB_TABLES['resource'],
                                userNameMatch + '%', resourceNameMatch + '%', sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                res_data = []
                for item in data:
                    res_data.append({
                        'userID': item['UserID'],
                        'userName': item['UserName'],
                        'resourceId': item['ResourceID'],
                        'resourceName': item['ResourceName']
                    })
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Records Fetched Successfully', 'data': res_data }), 200



@learns_from_bp.route('/addRecords', methods=['POST'])
def insert_records():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    records = request.get_json()
    
    if 'records' not in records:
        return jsonify({'error': 'Incorrect Body: Could not find records'}), 400
    
    values_to_insert = []
    for record in records['records']:
        userId = record.get('userId')
        resourceId = record.get('resourceId')
        
        if not userId or not resourceId:
            return jsonify({'error': 'Each record must have a userId or resourceId'}), 400
        
        values_to_insert.append((userId, resourceId))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (UserID, ResourceID)
                    VALUES (%s, %s)
                """.format(DB_TABLES['learns_from']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Inserted Successfully'}), 201

@learns_from_bp.route('/deleteRecordsByUserID', methods=['DELETE'])
def delete_records_by_user_id():
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
                """.format(DB_TABLES['learns_from']), (userId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Record(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Deleted Successfully'}), 200

@learns_from_bp.route('/deleteRecordsByResourceID', methods=['DELETE'])
def delete_records_by_resource_id():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    resourceId = data.get('resourceId')
    
    if not resourceId:
        return jsonify({'error': 'ResourceID must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE ResourceID = %s
                """.format(DB_TABLES['learns_from']), (resourceId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Record(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Deleted Successfully'}), 200