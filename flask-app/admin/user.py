from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

user_bp = Blueprint('user', __name__)
PER_PAGE = 10

def userExists(name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM {} WHERE Name = \'{}\'".format(DB_TABLES['user'], name))
            data = cur.fetchone()
            return data is not None

@user_bp.route('/', methods=['GET'])
def get_users():
    allowed_params = ['page', 'sort', 'sortBy', 'name', 'educationLevel', 'codingLevel', 'yearsCoding', 'age', 'gender', 'location']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='UserID', type=str)
    nameMatch = request.args.get('name', default='', type=str)
    educationLevel = request.args.get('educationLevel', default='', type=str)
    codingLevel = request.args.get('codingLevel', default='', type=str)
    minYearsCoding = request.args.get('yearsCoding', default=None, type=int)
    maxYearsCoding = request.args.get('yearsCoding', default=None, type=int)
    minAge = request.args.get('age', default=None, type=int)
    maxAge = request.args.get('age', default=None, type=int)
    gender = request.args.get('gender', default='', type=str)
    location = request.args.get('location', default='', type=str)

    educationLevelQuery = 'AND EducationLevel = \'{}\''.format(educationLevel) if educationLevel else ''
    codingLevelQuery = 'AND CodingLevel = \'{}\''.format(codingLevel) if codingLevel else ''
    minYearsCodingQuery = 'AND YearsCoding >= {}'.format(minYearsCoding) if minYearsCoding else ''
    maxYearsCodingQuery = 'AND YearsCoding <= {}'.format(maxYearsCoding) if maxYearsCoding else ''
    minAgeQuery = 'AND Age >= {}'.format(minAge) if minAge else ''
    maxAgeQuery = 'AND Age <= {}'.format(maxAge) if maxAge else ''
    genderQuery = 'AND Gender = \'{}\''.format(gender) if gender else ''
    locationQuery = 'AND Location = \'{}\''.format(location) if location else ''

    valid_sort_by = ['UserID', 'Name', 'YearsCoding', 'Age']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['user']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT * FROM {} WHERE Name LIKE \'{}\'
                    {} {} {} {} {} {} {} {}
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['user'], nameMatch + '%', educationLevelQuery, codingLevelQuery, minYearsCodingQuery, maxYearsCodingQuery, minAgeQuery, maxAgeQuery, genderQuery, locationQuery, sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                res_data = []
                for item in data:
                    res_data.append({
                        'id': item['UserID'],
                        'name': item['Name'],
                        'educationLevel': item['EducationLevel'],
                        'codingLevel': item['CodingLevel'],
                        'yearsCoding': item['YearsCoding'],
                        'age': item['Age'],
                        'gender': item['Gender'],
                        'location': item['Location']
                    })
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Users Fetched Successfully', 'data': res_data }), 200



@user_bp.route('/addUsers', methods=['POST'])
def insert_users():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    users = request.get_json()
    
    if 'users' not in users:
        return jsonify({'error': 'Incorrect Body: Could not find users'}), 400
    
    values_to_insert = []
    for user in users['users']:
        name = user.get('name')
        educationLevel = user.get('educationLevel')
        codingLevel = user.get('codingLevel')
        yearsCoding = user.get('yearsCoding')
        age = user.get('age')
        gender = user.get('gender')
        location = user.get('location')
        
        if not name:
            return jsonify({'error': 'Each User must have a name'}), 400

        if userExists(name):
            return jsonify({'error': 'User with name {} already exists'.format(name)}), 400
        
        values_to_insert.append((name, educationLevel, codingLevel, yearsCoding, age, gender, location))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (Name, EducationLevel, CodingLevel, YearsCoding, Age, Gender, Location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """.format(DB_TABLES['user']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Users Inserted Successfully'}), 201

@user_bp.route('/updateUser', methods=['PUT'])
def update_user():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    user_data = request.get_json()
    
    name = user_data.get('name')
    new_name = user_data.get('newName')
    education_level = user_data.get('educationLevel')
    coding_level = user_data.get('codingLevel')
    years_coding = user_data.get('yearsCoding')
    age = user_data.get('age')
    gender = user_data.get('gender')
    location = user_data.get('location')
    
    if not name:
        return jsonify({'error': 'User name must be provided'}), 400
    
    update_fields = []
    update_values = []
    
    if new_name:
        update_fields.append("Name = %s")
        update_values.append(new_name)
    
    if education_level:
        update_fields.append("EducationLevel = %s")
        update_values.append(education_level)
    
    if coding_level:
        update_fields.append("CodingLevel = %s")
        update_values.append(coding_level)
    
    if years_coding:
        update_fields.append("YearsCoding = %s")
        update_values.append(years_coding)
    
    if age:
        update_fields.append("Age = %s")
        update_values.append(age)
    
    if gender:
        update_fields.append("Gender = %s")
        update_values.append(age)
    
    if location:
        update_fields.append("Location = %s")
        update_values.append(location)
    
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    
    update_values.append(name)
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                if update_fields:
                    cur.execute("""
                        UPDATE {} SET {} WHERE Name = %s
                    """.format(DB_TABLES['user'], ", ".join(update_fields)), update_values)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'User Updated Successfully'}), 200

@user_bp.route('/deleteUser', methods=['DELETE'])
def delete_user():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'User name must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE Name = %s
                """.format(DB_TABLES['user']), (name,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'user not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'User Deleted Successfully'}), 200