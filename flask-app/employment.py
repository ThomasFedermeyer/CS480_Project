from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES
import pandas as pd

employment_bp = Blueprint('employment', __name__)
PER_PAGE = 10


@employment_bp.route('/getCompaniesAndProjects', methods=['GET'])
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
                companies = cur.fetchall()
                
                res_data = []
                for company in companies:
                    company_id = company['CompanyID']
                    
                    # Fetch projects for the company
                    cur.execute("SELECT * FROM {} WHERE CompanyID = {}".format(DB_TABLES['project'], company_id))
                    projects = cur.fetchall()
                    
                    project_list = []
                    for project in projects:
                        project_list.append({
                            'id': project['ProjectID'],
                            'name': project['Name'],
                            'description': project['Description'],
                            'duration': project['Duration'],
                            'budget': project['Budget']
                        })
                    
                    res_data.append({
                        'id': company['CompanyID'],
                        'name': company['Name'],
                        'profit': company['GrossProfit'],
                        'industry': company['Industry'],
                        'country': company['Country'],
                        'projects': project_list
                    })
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Companies Fetched Successfully', 'data': res_data, 'total_pages': total_pages}), 200

@employment_bp.route('/getEmploymentStatus', methods=['GET'])
def get_employment_status():
    distributionOf = request.args.get('distributionOf', default='CompanyName')
    byLocation = request.args.get('byLocation', default=False, type=bool)

    distributionColumnName = ''
    if distributionOf == 'CompanyName':
        distributionColumnName = 'Company.Name as CompanyName'
    elif distributionOf == 'RemotePolicy':
        distributionColumnName = 'RemotePolicy'
    elif distributionOf == 'WorkingTime':
        distributionColumnName = 'WorkingTime'
    elif distributionOf == 'DeveloperTypeName':
        distributionColumnName = 'DeveloperType.Name as DeveloperTypeName'
    else:
        return jsonify({'error': 'Invalid distributionOf parameter: ' + distributionOf}), 400
    
    locationColumnName = ', Location' if byLocation else ''

#     select RemotePolicy, WorkingTime, DeveloperType.Name as DeveloperTypeName,  Location from Position
# JOIN DeveloperType ON Position.DeveloperTypeID = DeveloperType.TypeID JOIN Company ON Position.CompanyID =
#  Company.CompanyID JOIN User ON Position.UserID = User.USerID;

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                query_string = """
                    SELECT {} {}
                    FROM {} JOIN {} ON Position.DeveloperTypeID = DeveloperType.TypeID
                    JOIN {} ON Position.CompanyID = Company.CompanyID
                    JOIN {} ON Position.UserID = User.UserID
                    """.format(distributionColumnName, locationColumnName, DB_TABLES['position'], DB_TABLES['developer_type'], DB_TABLES['company'], DB_TABLES['user'])
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                cols = [distributionOf] if not byLocation else [distributionOf, 'Location']
                df = pd.DataFrame(data, columns=cols)

                grouped_data = df.groupby(cols).size().reset_index(name='counts')
                res_data = grouped_data.to_dict(orient='records')
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500

    return jsonify({ 'error': False, 'message': 'Data Fetched Successfully', 'data': res_data }), 200


@employment_bp.route('/averageSalary', methods=['GET'])
def get_average_salary():
    groupBy = request.args.get('groupBy', default='DeveloperTypeName', type=str)
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                query_string = """
                    SELECT 
                        Position.Salary AS Salary,
                        DeveloperType.Name AS DeveloperTypeName,
                        User.YearsCoding AS YearsCoding,
                        Technology.Name AS TechName
                    FROM {} AS Position
                    JOIN {} AS DeveloperType ON Position.DeveloperTypeID = DeveloperType.TypeID
                    JOIN {} AS User ON Position.UserID = User.UserID
                    JOIN {} AS Project ON Project.CompanyID = Position.CompanyID
                    JOIN {} AS Project_Uses_Technology ON Project.ProjectID = Project_Uses_Technology.ProjectID
                    JOIN {} AS Technology ON Project_Uses_Technology.TechID = Technology.TechID
                """.format(DB_TABLES['position'], DB_TABLES['developer_type'], DB_TABLES['user'], DB_TABLES['project'], DB_TABLES['project_uses_technology'], DB_TABLES['technology'])
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                df = pd.DataFrame(data, columns=['Salary', groupBy])
                
                if groupBy == 'YearsCoding':
                    bins = [0, 1, 4, 9, 20, float('inf')]
                    labels = ['0-1', '2-4', '5-9', '10-20', 'Over 20']
                    df['YearsCodingGroup'] = pd.cut(df['YearsCoding'], bins=bins, labels=labels, right=False)
                    grouped_data = df.groupby('YearsCodingGroup')['Salary'].mean().reindex(labels, fill_value=0).reset_index(name='AvgSalary')
                    grouped_data['AvgSalary'] = grouped_data['AvgSalary'].fillna(0)
                elif groupBy in ['DeveloperTypeName', 'TechName']:
                    grouped_data = df.groupby(groupBy)['Salary'].mean().reset_index(name='AvgSalary')
                else:
                    return jsonify({'error': 'Invalid groupBy parameter: ' + groupBy}), 400
                
                res_data = grouped_data.to_dict(orient='records')
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None}), 500

    return jsonify({'error': False, 'message': 'Data Fetched Successfully', 'data': res_data}), 200