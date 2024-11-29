from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES
import pandas as pd

developer_profile_bp = Blueprint('developer_profile', __name__)


# Basic Demographics
@developer_profile_bp.route('/ageAndGenderByLevel', methods=['GET'])
def get_age_gender():
    allowed_params = ['demographic', 'codingLevelFilter']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
        
    
    demographicColumn = request.args.get('demographic', default='Age', type=str)
    codingLevelFilter = request.args.get('codingLevelFilter', default=None, type=str)

    codingLevelFilterQuery = 'WHERE CodingLevel = \'{}\''.format(codingLevelFilter) if codingLevelFilter else ''
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:

                query_string = """
                    SELECT UserID, {}
                    FROM {}
                    {}
                    """.format(demographicColumn, DB_TABLES['user'], codingLevelFilterQuery)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()

                df = pd.DataFrame(data, columns=['UserID', demographicColumn])

                if demographicColumn == 'Age':
                    bins = [0, 18, 25, 35, 45, 55, 65, 100]
                    labels = ['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '66-100']
                    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
                    grouped_data = df.groupby('AgeGroup').size().reset_index(name='counts')
                else:
                    gender_categories = ['M', 'F', 'O']
                    grouped_data = df.groupby(demographicColumn).size().reindex(gender_categories, fill_value=0).reset_index(name='counts')
                
                res_data = grouped_data.to_dict(orient='records')
                
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500

    return jsonify({ 'error': False, 'message': 'Data Fetched Successfully', 'data': res_data }), 200

@developer_profile_bp.route('/educationLevel', methods=['GET'])
def get_education_level():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                query_string = """
                    SELECT UserID, EducationLevel
                    FROM {}
                    """.format(DB_TABLES['user'])
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                df = pd.DataFrame(data, columns=['UserID', 'EducationLevel'])

                education_levels = [
                    'Primary/elementary school', 
                    'Secondary school', 
                    'Bachelor\'s degree', 
                    'Master\'s degree', 
                    'Professional degree', 
                    'Something else'
                ]
                
                grouped_data = df.groupby('EducationLevel').size().reindex(education_levels, fill_value=0).reset_index(name='counts')
                
                res_data = grouped_data.to_dict(orient='records')
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500

    return jsonify({ 'error': False, 'message': 'Data Fetched Successfully', 'data': res_data }), 200

@developer_profile_bp.route('/locationStats', methods=['GET'])
def get_location_stats():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                query_string = """
                    SELECT UserID, Location, YearsCoding
                    FROM {}
                    """.format(DB_TABLES['user'])
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                df = pd.DataFrame(data, columns=['UserID', 'Location', 'YearsCoding'])
                
                # Handle null values
                df['Location'].fillna('Other', inplace=True)
                df['YearsCoding'].fillna(0, inplace=True)
                
                # Group by location and calculate counts and average YearsCoding
                grouped_data = df.groupby('Location').agg(
                    counts=('UserID', 'size'),
                    AvgYearsCoding=('YearsCoding', 'mean')
                ).reset_index()
                
                res_data = grouped_data.to_dict(orient='records')
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500

    return jsonify({ 'error': False, 'message': 'Data Fetched Successfully', 'data': res_data }), 200

@developer_profile_bp.route('/yearsCodingDistribution', methods=['GET'])
def get_years_coding_distribution():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                query_string = """
                    SELECT UserID, YearsCoding
                    FROM {}
                    """.format(DB_TABLES['user'])
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                df = pd.DataFrame(data, columns=['UserID', 'YearsCoding'])
                
                df['YearsCoding'].fillna(0, inplace=True)

                bins = [0, 1, 4, 9, 20, float('inf')]
                labels = ['0-1', '1-4', '5-9', '10-20', 'Over 20']
                
                df['YearsCodingGroup'] = pd.cut(df['YearsCoding'], bins=bins, labels=labels, right=False)
                
                grouped_data = df.groupby('YearsCodingGroup').size().reset_index(name='counts')
                
                res_data = grouped_data.to_dict(orient='records')
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500

    return jsonify({ 'error': False, 'message': 'Data Fetched Successfully', 'data': res_data }), 200

# developer types
@developer_profile_bp.route('/developerTypesAndYearsCoding', methods=['GET'])
def get_developer_types():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                query_string = """
                    SELECT DeveloperType.Name AS DeveloperTypeName, Position.UserID AS UserID, User.YearsCoding AS YearsCoding
                    FROM {} LEFT JOIN {} ON DeveloperType.TypeID = Position.DeveloperTypeID
                    LEFT JOIN {} ON Position.UserID = User.UserID
                    """.format(DB_TABLES['developer_type'], DB_TABLES['position'], DB_TABLES['user'])
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                df = pd.DataFrame(data, columns=['UserID', 'DeveloperTypeName', 'YearsCoding'])
                df['YearsCoding'].fillna(0, inplace=True)
                
                grouped_data = df.groupby('DeveloperTypeName').agg(
                    counts=('UserID', lambda x: x.notnull().sum()),
                    AvgYearsCoding=('YearsCoding', 'mean')
                ).reset_index()

                res_data = grouped_data.to_dict(orient='records')
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500

    return jsonify({ 'error': False, 'message': 'Data Fetched Successfully', 'data': res_data }), 200

# learning
@developer_profile_bp.route('/learningResources', methods=['GET'])
def get_learning_resources():
    byLearning = request.args.get('byLearning', default=False, type=bool)
    byAge = request.args.get('byAge', default=False, type=bool)
    print("AGE IS", byAge)
    
    codingLevelQuery = "WHERE User.CodingLevel = 'Learning'" if byLearning else ''
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                query_string = """
                    SELECT Resource.Name AS ResourceName, Resource.Type AS ResourceType, User.UserID AS UserID, User.Age AS Age
                    FROM {} LEFT JOIN {} ON Resource.ResourceID = Learns_From.ResourceID
                    LEFT JOIN (SELECT * FROM {} {}) AS User ON Learns_From.UserID = User.UserID
                    """.format(DB_TABLES['resource'], DB_TABLES['learns_from'], DB_TABLES['user'], codingLevelQuery)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                df = pd.DataFrame(data, columns=['ResourceName', 'ResourceType', 'UserID', 'Age'])
                
                # Handle null values
                df['UserID'].fillna(0, inplace=True)
                df['Age'].fillna(-1, inplace=True)  # Use -1 to indicate missing age
                
                if byAge:
                    bins = [0, 18, 25, 35, 45, 55, 65, 100]
                    labels = ['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '66-100']
                    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
                    grouped_data = df[df['UserID'] != 0].groupby(['ResourceName', 'ResourceType', 'AgeGroup']).size().reset_index(name='counts')
                    
                    # Ensure all resource names, resource types, and age bins are included with count 0 if not present
                    all_resources = df[['ResourceName', 'ResourceType']].drop_duplicates()
                    all_age_groups = pd.DataFrame({'AgeGroup': labels})
                    all_combinations = all_resources.assign(key=1).merge(all_age_groups.assign(key=1), on='key').drop('key', axis=1)
                    grouped_data = all_combinations.merge(grouped_data, on=['ResourceName', 'ResourceType', 'AgeGroup'], how='left').fillna(0)
                    grouped_data['counts'] = grouped_data['counts'].astype(int)
                else:
                    grouped_data = df[df['UserID'] != 0].groupby(['ResourceName', 'ResourceType']).size().reset_index(name='counts')
                    
                    # Ensure all resource names and resource types are included with count 0 if not present
                    all_resources = df[['ResourceName', 'ResourceType']].drop_duplicates()
                    grouped_data = all_resources.merge(grouped_data, on=['ResourceName', 'ResourceType'], how='left').fillna(0)
                    grouped_data['counts'] = grouped_data['counts'].astype(int)
                
                res_data = grouped_data.to_dict(orient='records')
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500

    return jsonify({ 'error': False, 'message': 'Data Fetched Successfully', 'data': res_data }), 200
