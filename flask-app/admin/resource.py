from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

resource_bp = Blueprint('resource_bp', __name__)
PER_PAGE = 10

def resourceExists(name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM {} WHERE Name = \'{}\'".format(DB_TABLES['resource'], name))
            data = cur.fetchone()
            return data is not None

@resource_bp.route('/', methods=['GET'])
def get_resources():
    allowed_params = ['page', 'sort', 'sortBy', 'name', 'type']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='ResourceID', type=str)
    nameMatch = request.args.get('name', default='', type=str)
    resourceType = request.args.get('type', default='', type=str)

    resourceTypeQuery = 'AND Type = \'{}\''.format(resourceType) if resourceType else ''

    valid_sort_by = ['ResourceID', 'Name']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['resource']))
                total_count = cur.fetchone()['COUNT(*)']
                
                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT * FROM {} WHERE Name LIKE \'{}\'
                    {} ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['resource'], nameMatch + '%', resourceTypeQuery, sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                res_data = []
                for item in data:
                    res_data.append({
                        'id': item['ResourceID'],
                        'name': item['Name'],
                        'type': item['Type']
                    })
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Resources Fetched Successfully', 'data': res_data}), 200


@resource_bp.route('/addResources', methods=['POST'])
def add_resources():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    resources = request.get_json()
    
    if 'resources' not in resources:
        return jsonify({'error': 'Incorrect Body: Could not find resources'}), 400
    
    values_to_insert = []
    for resource in resources['resources']:
        name = resource.get('name')
        resourceType = resource.get('type')
        
        if not name:
            return jsonify({'error': 'Each Resource must have a name'}), 400


        if resourceExists(name):
            return jsonify({'error': 'Resource with name {} already exists'.format(name)}), 400
        
        values_to_insert.append((name, resourceType))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (Name, Type)
                    VALUES (%s, %s)
                """.format(DB_TABLES['resource']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Resources Inserted Successfully'}), 201


@resource_bp.route('/updateResource', methods=['PUT'])
def update_resource():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    resource_data = request.get_json()
    
    name = resource_data.get('name')
    new_name = resource_data.get('newName')
    resourceType = resource_data.get('type')
    
    if not name:
        return jsonify({'error': 'Resource name must be provided'}), 400
    
    update_fields = []
    update_values = []
    
    if new_name:
        update_fields.append("Name = %s")
        update_values.append(new_name)
    
    if resourceType:
        update_fields.append("Type = %s")
        update_values.append(resourceType)
    
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    
    update_values.append(name)
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    UPDATE {} SET {} WHERE Name = %s
                """.format(DB_TABLES['resource'], ", ".join(update_fields)), update_values)
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Resource not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Resource Updated Successfully'}), 200


@resource_bp.route('/deleteResource', methods=['DELETE'])
def delete_resource():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Resource name must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE Name = %s
                """.format(DB_TABLES['resource']), (name,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Resource not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Resource Deleted Successfully'}), 200