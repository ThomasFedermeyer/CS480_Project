from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

developer_type_bp = Blueprint('developer_type', __name__)
PER_PAGE = 10

def developerTypeExists(name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM {} WHERE Name = \'{}\'".format(DB_TABLES['developer_type'], name))
            data = cur.fetchone()
            return data is not None

@developer_type_bp.route('/', methods=['GET'])
def get_developer_types():
    allowed_params = ['page', 'sort', 'sortBy', 'name', 'minPopularity', 'maxPopularity', 'minExperience']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='TypeID', type=str)
    nameMatch = request.args.get('name', default='', type=str)
    minPopularity = request.args.get('minPopularity', default=0, type=int)
    maxPopularity = request.args.get('maxPopularity', default=10, type=int)
    minExperience = request.args.get('minExperience', default=0, type=int)

    valid_sort_by = ['TypeID', 'Name', 'PopularityRating', 'RequiredExperience']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['developer_type']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT * FROM {} WHERE Name LIKE \'{}\' AND 
                    PopularityRating >= {} AND
                    PopularityRating <= {} AND 
                    RequiredExperience >= {} 
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['developer_type'], nameMatch + '%', minPopularity, maxPopularity, minExperience, sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                res_data = [{ 'id': item['TypeID'], 'name': item['Name'], 'popularity': item['PopularityRating'], 'experience': item['RequiredExperience'] } for item in data]
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Developer Types Fetched Successfully', 'data': res_data }), 200



@developer_type_bp.route('/addDeveloperTypes', methods=['POST'])
def insert_developer_types():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    developer_types = request.get_json()
    
    if 'developerTypes' not in developer_types:
        return jsonify({'error': 'Incorrect Body: Could not find developerTypes'}), 400
    
    values_to_insert = []
    for developer_type in developer_types['developerTypes']:
        name = developer_type.get('name')
        popularity = developer_type.get('popularity', 0)
        experience = developer_type.get('experience', 0)
        
        if not name:
            return jsonify({'error': 'Each developer type must have a name'}), 400

        if developerTypeExists(name):
            return jsonify({'error': 'Developer Type with name {} already exists'.format(name)}), 400
        
        values_to_insert.append((name, popularity, experience))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (Name, PopularityRating, RequiredExperience)
                    VALUES (%s, %s, %s)
                """.format(DB_TABLES['developer_type']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Developer Types Inserted Successfully'}), 201

@developer_type_bp.route('/updateDeveloperType', methods=['PUT'])
def update_developer_type():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    developer_type = request.get_json()
    
    name = developer_type.get('name')
    new_name = developer_type.get('newName')
    popularity = developer_type.get('popularity')
    experience = developer_type.get('experience')
    
    if not name:
        return jsonify({'error': 'Developer type must have a name'}), 400
    
    update_fields = []
    update_values = []

    if new_name is not None:
        update_fields.append("Name = %s")
        update_values.append(new_name)
    
    if popularity is not None:
        update_fields.append("PopularityRating = %s")
        update_values.append(popularity)
    
    if experience is not None:
        update_fields.append("RequiredExperience = %s")
        update_values.append(experience)
    
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    
    update_values.append(name)
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    UPDATE {} SET {} WHERE Name = %s
                """.format(DB_TABLES['developer_type'], ", ".join(update_fields)), update_values)
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Developer type not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Developer Type Updated Successfully'}), 200

@developer_type_bp.route('/deleteDeveloperType', methods=['DELETE'])
def delete_developer_type():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Developer type must have a name'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE Name = %s
                """.format(DB_TABLES['developer_type']), (name,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Developer type not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Developer Type Deleted Successfully'}), 200
