from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

company_bp = Blueprint('company_bp', __name__)
PER_PAGE = 10

def companyExists(name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM {} WHERE Name = \'{}\'".format(DB_TABLES['company'], name))
            data = cur.fetchone()
            return data is not None

@company_bp.route('/', methods=['GET'])
def get_companies():
    allowed_params = ['page', 'sort', 'sortBy', 'name', 'minProfit', 'maxProfit', 'industry', 'country']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='CompanyID', type=str)
    nameMatch = request.args.get('name', default='', type=str)
    minProfit = request.args.get('minProfit', default=None, type=int)
    maxProfit = request.args.get('maxProfit', default=None, type=int)
    industry = request.args.get('industry', default='', type=str)
    country = request.args.get('country', default='', type=str)

    minProfitQuery = 'AND GrossProfit >= {}'.format(minProfit) if minProfit else ''
    maxProfitQuery = 'AND GrossProfit <= {}'.format(maxProfit) if maxProfit else ''
    industryQuery = 'AND Industry LIKE \'{}%\''.format(industry) if industry else ''
    countryQuery = 'AND Country LIKE \'{}%\''.format(country) if country else ''

    valid_sort_by = ['CompanyID', 'Name', 'GrossProfit']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['company']))
                total_count = cur.fetchone()['COUNT(*)']
                
                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT * FROM {} WHERE Name LIKE \'{}\'
                    {} {} {} {}
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['company'], nameMatch + '%', minProfitQuery, maxProfitQuery, industryQuery, countryQuery, sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                res_data = []
                for item in data:
                    res_data.append({
                        'id': item['CompanyID'],
                        'name': item['Name'],
                        'profit': item['GrossProfit'],
                        'industry': item['Industry'],
                        'country': item['Country']
                    })
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Companies Fetched Successfully', 'data': res_data}), 200


@company_bp.route('/addCompanies', methods=['POST'])
def add_companies():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    companies = request.get_json()
    
    if 'companies' not in companies:
        return jsonify({'error': 'Incorrect Body: Could not find companies'}), 400
    
    values_to_insert = []
    for company in companies['companies']:
        name = company.get('name')
        profit = company.get('profit', None)
        industry = company.get('industry', None)
        country = company.get('country', None)
        
        if not name:
            return jsonify({'error': 'Each company must have a name'}), 400


        if companyExists(name):
            return jsonify({'error': 'Company with name {} already exists'.format(name)}), 400
        
        values_to_insert.append((name, profit, industry, country))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (Name, GrossProfit, Industry, Country)
                    VALUES (%s, %s, %s, %s)
                """.format(DB_TABLES['company']), values_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Companies Inserted Successfully'}), 201


@company_bp.route('/updateCompany', methods=['PUT'])
def update_company():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    company_data = request.get_json()
    
    name = company_data.get('name')
    new_name = company_data.get('newName')
    profit = company_data.get('profit')
    industry = company_data.get('industry')
    country = company_data.get('country')
    
    if not name:
        return jsonify({'error': 'Company name must be provided'}), 400
    
    update_fields = []
    update_values = []
    
    if new_name:
        update_fields.append("Name = %s")
        update_values.append(new_name)
    
    if profit:
        update_fields.append("GrossProfit = %s")
        update_values.append(profit)
    
    if industry:
        update_fields.append("Industry = %s")
        update_values.append(industry)
    
    if country:
        update_fields.append("Country = %s")
        update_values.append(country)
    
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    
    update_values.append(name)
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    UPDATE {} SET {} WHERE Name = %s
                """.format(DB_TABLES['company'], ", ".join(update_fields)), update_values)
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Company not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Company Updated Successfully'}), 200


@company_bp.route('/deleteCompany', methods=['DELETE'])
def delete_company():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Company name must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE Name = %s
                """.format(DB_TABLES['company']), (name,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'company not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Company Deleted Successfully'}), 200