from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

resource_uses_tool_bp = Blueprint('resource_uses_tool', __name__)
PER_PAGE = 10

@resource_uses_tool_bp.route('/', methods=['GET'])
def get_records():
    allowed_params = ['page', 'sort', 'sortBy', 'resourceName', 'toolName']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='ResourceID', type=str)
    resourceNameMatch = request.args.get('resourceName', default='', type=str)
    toolNameMatch = request.args.get('toolName', default='', type=str)

    valid_sort_by = ['ResourceID' , 'ResourceName', 'ToolName']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['resource_uses_tool']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT resource_uses_tool.ResourceID AS ResourceID, Resource.Name AS ResourceName, resource_uses_tool.toolId AS ToolID, Tool.Name AS ToolName
                    FROM {} JOIN {} ON {}.ResourceID = {}.ResourceID JOIN {} ON {}.ToolID = {}.ToolID
                    WHERE Resource.Name LIKE \'{}\' AND
                    Tool.Name LIKE \'{}\' 
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['resource_uses_tool'], DB_TABLES['resource'], DB_TABLES['resource_uses_tool'], DB_TABLES['resource'], DB_TABLES['tool'], DB_TABLES['resource_uses_tool'], DB_TABLES['tool'],
                                resourceNameMatch + '%', toolNameMatch + '%', sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                res_data = []
                for item in data:
                    res_data.append({
                        'resourceId': item['ResourceID'],
                        'resourceName': item['ResourceName'],
                        'toolId': item['ToolID'],
                        'toolName': item['ToolName']
                    })
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Records Fetched Successfully', 'data': res_data }), 200



@resource_uses_tool_bp.route('/addRecords', methods=['POST'])
def insert_records():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    records = request.get_json()
    
    if 'records' not in records:
        return jsonify({'error': 'Incorrect Body: Could not find records'}), 400
    
    values_to_insert = []
    for record in records['records']:
        resourceId = record.get('resourceId')
        toolId = record.get('toolId')
        
        if not resourceId or not toolId:
            return jsonify({'error': 'Each record must have a resourceId or toolId'}), 400
        
        values_to_insert.append((resourceId, toolId))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (ResourceID, ToolID)
                    VALUES (%s, %s)
                """.format(DB_TABLES['resource_uses_tool']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Inserted Successfully'}), 201

@resource_uses_tool_bp.route('/deleteRecordsByResourceID', methods=['DELETE'])
def delete_records_by_resource_id():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    resourceId = data.get('resourceId')
    
    if not resourceId:
        return jsonify({'error': 'resourceId must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE ResourceID = %s
                """.format(DB_TABLES['resource_uses_tool']), (resourceId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Record(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Deleted Successfully'}), 200

@resource_uses_tool_bp.route('/deleteRecordsByToolID', methods=['DELETE'])
def delete_records_by_tool_id():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    toolId = data.get('toolId')
    
    if not toolId:
        return jsonify({'error': 'toolId must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE ToolID = %s
                """.format(DB_TABLES['resource_uses_tool']), (toolId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Record(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Deleted Successfully'}), 200