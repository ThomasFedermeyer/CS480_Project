from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

technology_bp = Blueprint('technology', __name__)
PER_PAGE = 10

def technologyExists(name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM {} WHERE Name = \'{}\'".format(DB_TABLES['technology'], name))
            data = cur.fetchone()
            return data is not None

def get_technology_type_id(technology_type_name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT TypeID FROM {} WHERE Name = %s
            """.format(DB_TABLES['technology_type']), (technology_type_name,))
            result = cur.fetchone()
            if result:
                return result['TypeID']
            else:
                return None

@technology_bp.route('/', methods=['GET'])
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

    return jsonify({ 'error': False, 'message': 'Technologies Fetched Successfully', 'data': res_data }), 200



@technology_bp.route('/addTechnologies', methods=['POST'])
def insert_technologies():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    technologies = request.get_json()
    
    if 'technologies' not in technologies:
        return jsonify({'error': 'Incorrect Body: Could not find technologies'}), 400
    
    values_to_insert = []
    for technology in technologies['technologies']:
        name = technology.get('name')
        dateOfRelease = technology.get('dateOfRelease')
        technologyType = technology.get('type')
        
        if not name:
            return jsonify({'error': 'Each technology must have a name'}), 400

        if technologyExists(name):
            return jsonify({'error': 'Technology with name {} already exists'.format(name)}), 400
        
        technologyTypeId = get_technology_type_id(technologyType)
        if not technologyTypeId:
            return jsonify({'error': 'Technology Type with name {} does not exist'.format(technologyType)}), 400
        
        values_to_insert.append((name, dateOfRelease, technologyTypeId))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (Name, DateOfRelease, TypeID)
                    VALUES (%s, %s, %s)
                """.format(DB_TABLES['technology']), values_to_insert)

                first_id = cur.lastrowid
                last_id = first_id + len(values_to_insert) - 1
                
                inserted_ids = list(range(first_id, last_id + 1))
                use_cases_to_insert = []
                for i, technology_id in enumerate(inserted_ids):
                    useCases = technologies['technologies'][i].get('useCases')
                    if useCases:
                        use_cases_to_insert.extend([(technology_id, useCase.strip()) for useCase in useCases])
                
                if len(use_cases_to_insert) > 0:
                    print(use_cases_to_insert)
                    cur.executemany("""
                            INSERT INTO {} (TechID, UseCase)
                            VALUES (%s, %s)
                        """.format(DB_TABLES['technology_use_case']), use_cases_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Technologies Inserted Successfully'}), 201

@technology_bp.route('/updateTechnology', methods=['PUT'])
def update_technology():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    technology_data = request.get_json()
    
    name = technology_data.get('name')
    new_name = technology_data.get('newName')
    dateOfRelease = technology_data.get('dateOfRelease')
    technologyType = technology_data.get('type')
    technologyTypeId = get_technology_type_id(technologyType)    
    useCases = technology_data.get('useCases')
    
    if not name:
        return jsonify({'error': 'Technology name must be provided'}), 400
    
    update_fields = []
    update_values = []
    
    if new_name:
        update_fields.append("Name = %s")
        update_values.append(new_name)
    
    if dateOfRelease:
        update_fields.append("DateOfRelease = %s")
        update_values.append(dateOfRelease)
    
    if technologyType:
        if not technologyTypeId:
            return jsonify({'error': 'Technology Type with name {} does not exist'.format(technologyType)}), 400
        
        update_fields.append("TypeID = %s")
        update_values.append(technologyTypeId)
    
    if not update_fields and not useCases:
        return jsonify({'error': 'No fields to update'}), 400
    
    update_values.append(name)
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                if update_fields:
                    cur.execute("""
                        UPDATE {} SET {} WHERE Name = %s
                    """.format(DB_TABLES['technology'], ", ".join(update_fields)), update_values)
                
                if useCases is not None:
                    cur.execute("""
                        DELETE FROM {} WHERE TechID = (SELECT TechID FROM {} WHERE Name = %s)
                    """.format(DB_TABLES['technology_use_case'], DB_TABLES['technology']), (name,))
                    
                    if len(useCases) > 0:
                        technology_id_query = "SELECT TechID FROM {} WHERE Name = %s".format(DB_TABLES['technology'])
                        cur.execute(technology_id_query, (name,))
                        technology_id = cur.fetchone()['TechID']
                        
                        use_cases_to_insert = [(technology_id, useCase.strip()) for useCase in useCases]
                        cur.executemany("""
                            INSERT INTO {} (TechID, UseCase)
                            VALUES (%s, %s)
                        """.format(DB_TABLES['technology_use_case']), use_cases_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Technology Updated Successfully'}), 200

@technology_bp.route('/deleteTechnology', methods=['DELETE'])
def delete_technology():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Technology name must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE Name = %s
                """.format(DB_TABLES['technology']), (name,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Technology not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Technology Deleted Successfully'}), 200