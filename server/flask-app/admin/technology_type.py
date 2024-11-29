from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

technology_type_bp = Blueprint('technology_type', __name__)
PER_PAGE = 10

def technologyTypeExists(name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM {} WHERE Name = \'{}\'".format(DB_TABLES['technology_type'], name))
            data = cur.fetchone()
            return data is not None

@technology_type_bp.route('/', methods=['GET'])
def get_technology_types():
    allowed_params = ['page', 'sort', 'sortBy', 'name']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='TypeID', type=str)
    nameMatch = request.args.get('name', default='', type=str)

    valid_sort_by = ['TypeID', 'Name']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['technology_type']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT * FROM {} WHERE Name LIKE \'{}\'
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['technology_type'], nameMatch + '%', sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                res_data = [{ 'id': item['TypeID'], 'name': item['Name'], 'description': item['Description'] } for item in data]
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Technology Types Fetched Successfully', 'data': res_data }), 200



@technology_type_bp.route('/addTechnologyTypes', methods=['POST'])
def insert_technology_types():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    technology_types = request.get_json()
    
    if 'technologyTypes' not in technology_types:
        return jsonify({'error': 'Incorrect Body: Could not find technologyTypes'}), 400
    
    values_to_insert = []
    for technology_type in technology_types['technologyTypes']:
        name = technology_type.get('name')
        description = technology_type.get('description', None)
        
        if not name:
            return jsonify({'error': 'Each Technology type must have a name'}), 400

        if technologyTypeExists(name):
            return jsonify({'error': 'Technology Type with name {} already exists'.format(name)}), 400
        
        values_to_insert.append((name, description))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (Name, Description)
                    VALUES (%s, %s)
                """.format(DB_TABLES['technology_type']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Technology Types Inserted Successfully'}), 201

@technology_type_bp.route('/updateTechnologyType', methods=['PUT'])
def update_technology_type():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    technology_type = request.get_json()
    
    name = technology_type.get('name')
    new_name = technology_type.get('newName')
    description = technology_type.get('description')
    
    if not name:
        return jsonify({'error': 'Technology type must have a name'}), 400
    
    update_fields = []
    update_values = []
    
    if new_name is not None:
        update_fields.append("Name = %s")
        update_values.append(new_name)
    
    if description is not None:
        update_fields.append("Description = %s")
        update_values.append(description)
    
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    
    update_values.append(name)
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    UPDATE {} SET {} WHERE Name = %s
                """.format(DB_TABLES['technology_type'], ", ".join(update_fields)), update_values)
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Technology type not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Technology Type Updated Successfully'}), 200

@technology_type_bp.route('/deleteTechnologyType', methods=['DELETE'])
def delete_technology_type():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Technology type must have a name'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE Name = %s
                """.format(DB_TABLES['technology_type']), (name,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Technology type not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Technology Type Deleted Successfully'}), 200
