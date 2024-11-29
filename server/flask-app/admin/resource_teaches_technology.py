from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

resource_teaches_technology_bp = Blueprint('resource_teaches_technology', __name__)
PER_PAGE = 10

@resource_teaches_technology_bp.route('/', methods=['GET'])
def get_records():
    allowed_params = ['page', 'sort', 'sortBy', 'resourceName', 'techName']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='ResourceID', type=str)
    resourceNameMatch = request.args.get('resourceName', default='', type=str)
    techNameMatch = request.args.get('techName', default='', type=str)

    valid_sort_by = ['ResourceID' , 'ResourceName', 'TechName']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['resource_teaches_technology']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT Resource_Teaches_Technology.ResourceID AS ResourceID, Resource.Name AS ResourceName, Resource_Teaches_Technology.TechID AS TechID, Technology.Name AS TechName
                    FROM {} JOIN {} ON {}.ResourceID = {}.ResourceID JOIN {} ON {}.TechID = {}.TechID
                    WHERE Resource.Name LIKE \'{}\' AND
                    Technology.Name LIKE \'{}\' 
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['resource_teaches_technology'], DB_TABLES['resource'], DB_TABLES['resource_teaches_technology'], DB_TABLES['resource'], DB_TABLES['technology'], DB_TABLES['resource_teaches_technology'], DB_TABLES['technology'],
                                resourceNameMatch + '%', techNameMatch + '%', sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                res_data = []
                for item in data:
                    res_data.append({
                        'resourceId': item['ResourceID'],
                        'resourceName': item['ResourceName'],
                        'techId': item['TechID'],
                        'techName': item['TechName']
                    })
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Records Fetched Successfully', 'data': res_data }), 200



@resource_teaches_technology_bp.route('/addRecords', methods=['POST'])
def insert_records():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    records = request.get_json()
    
    if 'records' not in records:
        return jsonify({'error': 'Incorrect Body: Could not find records'}), 400
    
    values_to_insert = []
    for record in records['records']:
        resourceId = record.get('resourceId')
        techId = record.get('techId')
        
        if not resourceId or not techId:
            return jsonify({'error': 'Each record must have a resourceId or techId'}), 400
        
        values_to_insert.append((resourceId, techId))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (ResourceID, TechID)
                    VALUES (%s, %s)
                """.format(DB_TABLES['resource_teaches_technology']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Inserted Successfully'}), 201

@resource_teaches_technology_bp.route('/deleteRecordsByResourceID', methods=['DELETE'])
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
                """.format(DB_TABLES['resource_teaches_technology']), (resourceId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Record(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Deleted Successfully'}), 200

@resource_teaches_technology_bp.route('/deleteRecordsByTechID', methods=['DELETE'])
def delete_records_by_technology_id():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    techId = data.get('techId')
    
    if not techId:
        return jsonify({'error': 'techId must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE TechID = %s
                """.format(DB_TABLES['resource_teaches_technology']), (techId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Record(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Deleted Successfully'}), 200