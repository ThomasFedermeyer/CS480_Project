from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

technology_dependency_bp = Blueprint('technology_dependency', __name__)
PER_PAGE = 10

@technology_dependency_bp.route('/', methods=['GET'])
def get_records():
    allowed_params = ['page', 'sort', 'sortBy', 'dependentTechName', 'supportingTechName']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='DependentTechID', type=str)
    dependentTechNameMatch = request.args.get('dependentTechName', default='', type=str)
    supportingTechNameMatch = request.args.get('supportingTechName', default='', type=str)

    valid_sort_by = ['DependentTechID' , 'DependentTechName', 'SupportingTechName']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['technology_dependency']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT DependentTechID, dt.Name AS DependentTechName, SupportingTechID, st.Name AS SupportingTechName
                    FROM {} JOIN {} dt ON {}.DependentTechID = dt.TechID JOIN {} st ON {}.SupportingTechID = st.TechID
                    WHERE dt.Name LIKE \'{}\' AND
                    st.Name LIKE \'{}\' 
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['technology_dependency'], DB_TABLES['technology'], DB_TABLES['technology_dependency'], DB_TABLES['technology'], DB_TABLES['technology_dependency'],
                                dependentTechNameMatch + '%', supportingTechNameMatch + '%', sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                res_data = []
                for item in data:
                    res_data.append({
                        'dependentTechId': item['DependentTechID'],
                        'dependentTechName': item['DependentTechName'],
                        'supportingTechID': item['SupportingTechID'],
                        'supportingTechName': item['SupportingTechName']
                    })
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Records Fetched Successfully', 'data': res_data }), 200



@technology_dependency_bp.route('/addRecords', methods=['POST'])
def insert_records():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    records = request.get_json()
    
    if 'records' not in records:
        return jsonify({'error': 'Incorrect Body: Could not find records'}), 400
    
    values_to_insert = []
    for record in records['records']:
        dependentTechId = record.get('dependentTechId')
        supportingTechId = record.get('supportingTechId')
        
        if not dependentTechId or not supportingTechId:
            return jsonify({'error': 'Each record must have a dependentTechId or supportingTechId'}), 400
        
        values_to_insert.append((dependentTechId, supportingTechId))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (DependentTechId, SupportingTechId)
                    VALUES (%s, %s)
                """.format(DB_TABLES['technology_dependency']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Inserted Successfully'}), 201

@technology_dependency_bp.route('/deleteRecordsByDependentTechID', methods=['DELETE'])
def delete_records_by_dependent_tech_id():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    dependentTechId = data.get('dependentTechId')
    
    if not dependentTechId:
        return jsonify({'error': 'dependentTechId must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE DependentTechID = %s
                """.format(DB_TABLES['technology_dependency']), (dependentTechId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Record(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Deleted Successfully'}), 200

@technology_dependency_bp.route('/deleteRecordsBySupportingTechID', methods=['DELETE'])
def delete_records_by_supporting_tech_id():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    supportingTechId = data.get('supportingTechId')
    
    if not supportingTechId:
        return jsonify({'error': 'supportingTechId must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE SupportingTechID = %s
                """.format(DB_TABLES['technology_dependency']), (supportingTechId,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Record(s) not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Records Deleted Successfully'}), 200