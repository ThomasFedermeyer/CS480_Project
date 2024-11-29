from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

project_bp = Blueprint('project', __name__)
PER_PAGE = 10

def projectExists(name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM {} WHERE Name = \'{}\'".format(DB_TABLES['project'], name))
            data = cur.fetchone()
            return data is not None

def get_project_company_id(project_company_name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT CompanyID FROM {} WHERE Name = %s
            """.format(DB_TABLES['company']), (project_company_name,))
            result = cur.fetchone()
            if result:
                return result['CompanyID']
            else:
                return None

@project_bp.route('/', methods=['GET'])
def get_projects():
    allowed_params = ['page', 'sort', 'sortBy', 'name', 'minDuration', 'maxDuration', 'minBudget', 'maxBudget', 'company']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='ProjectID', type=str)
    nameMatch = request.args.get('name', default='', type=str)
    minDuration = request.args.get('minDuration', default=None, type=int)
    maxDuration = request.args.get('maxDuration', default=None, type=int)
    minBudget = request.args.get('minBudget', default=None, type=int)
    maxBudget = request.args.get('maxBudget', default=None, type=int)
    company = request.args.get('company', default=None, type=str)

    minDurationQuery = 'AND Duration >= {}'.format(minDuration) if minDuration else ''
    maxDurationQuery = 'AND Duration <= {}'.format(maxDuration) if maxDuration else ''
    minBudgetQuery = 'AND Budget >= {}'.format(minBudget) if minBudget else ''
    maxBudgetQuery = 'AND Budget <= {}'.format(maxBudget) if maxBudget else ''
    companyQuery = 'AND Company.Name = {}'.format(company) if company else ''

    valid_sort_by = ['ProjectID', 'ProjectName', 'Duration', 'Budget']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['project']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT ProjectID, Project.Name as ProjectName, Description, Duration, Budget, Company.Name as CompanyName 
                    FROM {} JOIN {} ON {}.CompanyID = {}.CompanyID
                    WHERE Project.Name LIKE \'{}\'
                    {} {} {} {} {}
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['project'], DB_TABLES['company'], DB_TABLES['project'], DB_TABLES['company'],
                                nameMatch + '%', minDurationQuery, maxDurationQuery, minBudgetQuery, maxBudgetQuery, companyQuery, sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                res_data = []
                for item in data:
                    res_data.append({
                        'id': item['ProjectID'],
                        'name': item['ProjectName'],
                        'description': item['Description'],
                        'duration': item['Duration'],
                        'budget': item['Budget'],
                        'company': item['CompanyName']
                    })
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Projects Fetched Successfully', 'data': res_data }), 200



@project_bp.route('/addProjects', methods=['POST'])
def insert_projects():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    projects = request.get_json()
    
    if 'projects' not in projects:
        return jsonify({'error': 'Incorrect Body: Could not find projects'}), 400
    
    values_to_insert = []
    for project in projects['projects']:
        name = project.get('name')
        description = project.get('description')
        duration = project.get('duration')
        budget = project.get('budget')
        company = project.get('company')
        
        if not name:
            return jsonify({'error': 'Each project must have a name'}), 400

        if projectExists(name):
            return jsonify({'error': 'Project with name {} already exists'.format(name)}), 400
        
        companyId = get_project_company_id(company)
        if not companyId:
            return jsonify({'error': 'Company with name {} does not exist'.format(company)}), 400
        
        values_to_insert.append((name, description, duration, budget, companyId))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (Name, Description, Duration, Budget, CompanyID)
                    VALUES (%s, %s, %s, %s, %s)
                """.format(DB_TABLES['project']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Projects Inserted Successfully'}), 201

@project_bp.route('/updateProject', methods=['PUT'])
def update_project():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    project_data = request.get_json()
    
    name = project_data.get('name')
    new_name = project_data.get('newName')
    description = project_data.get('description')
    duration = project_data.get('duration')
    budget = project_data.get('budget')
    company = project_data.get('company')
    
    if not name:
        return jsonify({'error': 'project name must be provided'}), 400
    
    update_fields = []
    update_values = []
    
    if new_name:
        update_fields.append("Name = %s")
        update_values.append(new_name)
    
    if description:
        update_fields.append("Description = %s")
        update_values.append(description)
    
    if duration:
        update_fields.append("Duration = %s")
        update_values.append(duration)
    
    if budget:
        update_fields.append("Budget = %s")
        update_values.append(budget)
    
    if company:
        companyId = get_project_company_id(company)
        if not companyId:
            return jsonify({'error': 'Company with name {} does not exist'.format(company)}), 400
        
        update_fields.append("CompanyID = %s")
        update_values.append(companyId)
    
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    
    update_values.append(name)
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                if update_fields:
                    cur.execute("""
                        UPDATE {} SET {} WHERE Name = %s
                    """.format(DB_TABLES['project'], ", ".join(update_fields)), update_values)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Project Updated Successfully'}), 200

@project_bp.route('/deleteProject', methods=['DELETE'])
def delete_project():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Project name must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE Name = %s
                """.format(DB_TABLES['project']), (name,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Project not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Project Deleted Successfully'}), 200