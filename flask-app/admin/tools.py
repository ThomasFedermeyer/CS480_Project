from flask import Blueprint, request, jsonify
from db import get_db_connection, DB_TABLES

tool_bp = Blueprint('tool', __name__)
PER_PAGE = 10

def toolExists(name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM {} WHERE Name = \'{}\'".format(DB_TABLES['tool'], name))
            data = cur.fetchone()
            return data is not None

@tool_bp.route('/', methods=['GET'])
def get_tools():
    allowed_params = ['page', 'sort', 'sortBy', 'name', 'type', 'sync', 'fromDate', 'toDate']
    for param in request.args:
        if param not in allowed_params:
            return jsonify({'error': 'Invalid query parameter: ' + param}), 400
    
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='asc', type=str)
    sortBy = request.args.get('sortBy', default='ToolID', type=str)
    nameMatch = request.args.get('name', default='', type=str)
    toolType = request.args.get('type', default='', type=str)
    sync = request.args.get('sync', default=None, type=str)
    fromDate = request.args.get('fromDate', default='', type=str)
    toDate = request.args.get('toDate', default='', type=str)

    toolTypeQuery = 'AND Type = \'{}\''.format(toolType) if toolType else ''
    syncQuery = 'AND Sync = \'{}\''.format(sync) if sync else ''
    fromDateQuery = 'AND DateOfRelease >= \'{}\''.format(fromDate) if fromDate else ''
    toDateQuery = 'AND DateOfRelease <= \'{}\''.format(toDate) if toDate else ''

    valid_sort_by = ['ToolID', 'Name', 'DateOfRelease']
    if sortBy not in valid_sort_by:
        return jsonify({'error': 'Invalid sortBy parameter: ' + sortBy}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM {}".format(DB_TABLES['tool']))
                total_count = cur.fetchone()['COUNT(*)']
                

                offset = (page - 1) * PER_PAGE
                limit = PER_PAGE

                query_string = """
                    SELECT * FROM {} NATURAL LEFT JOIN {} WHERE Name LIKE \'{}\'
                    {} {} {} {}
                    ORDER BY {} {} LIMIT {} OFFSET {}
                    """.format(DB_TABLES['tool'], DB_TABLES['tool_primary_purpose'],
                         nameMatch + '%', toolTypeQuery, syncQuery, fromDateQuery, toDateQuery, sortBy, sort, limit, offset)
                
                print(query_string)
                cur.execute(query_string)
                data = cur.fetchall()
                
                grouped_data = {}
                for item in data:
                    if item['ToolID'] not in grouped_data:
                        grouped_data[item['ToolID']] = {
                            'id': item['ToolID'],
                            'name': item['Name'],
                            'type': item['Type'],
                            'sync': item['SyncCapability'],
                            'dateOfRelease': item['DateOfRelease'],
                            'primaryPurposes': ''
                        }
                    if item['PrimaryPurpose']:
                        grouped_data[item['ToolID']]['primaryPurposes'] += ' | ' + item['PrimaryPurpose']
                
                res_data = list(grouped_data.values())
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({ 'error': True, 'message': 'Error Occurred: ' + str(e), 'data': None }), 500
            
    
    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    return jsonify({ 'error': False, 'message': 'Tools Fetched Successfully', 'data': res_data }), 200



@tool_bp.route('/addTools', methods=['POST'])
def insert_tools():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    tools = request.get_json()
    
    if 'tools' not in tools:
        return jsonify({'error': 'Incorrect Body: Could not find tools'}), 400
    
    values_to_insert = []
    for tool in tools['tools']:
        name = tool.get('name')
        toolType = tool.get('type')
        sync = tool.get('sync')
        dateOfRelease = tool.get('dateOfRelease')
        
        if not name:
            return jsonify({'error': 'Each Tool must have a name'}), 400

        if toolExists(name):
            return jsonify({'error': 'Tool with name {} already exists'.format(name)}), 400
        
        values_to_insert.append((name, toolType, sync, dateOfRelease))
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.executemany("""
                    INSERT INTO {} (Name, Type, SyncCapability, DateOfRelease)
                    VALUES (%s, %s, %s, %s)
                """.format(DB_TABLES['tool']), values_to_insert)

                first_id = cur.lastrowid
                last_id = first_id + len(values_to_insert) - 1
                
                inserted_ids = list(range(first_id, last_id + 1))
                primary_purposes_to_insert = []
                for i, tool_id in enumerate(inserted_ids):
                    primaryPurposes = tools['tools'][i].get('primaryPurposes')
                    if primaryPurposes:
                        primary_purposes_to_insert.extend([(tool_id, purpose.strip()) for purpose in primaryPurposes])
                
                if len(primary_purposes_to_insert) > 0:
                    print(primary_purposes_to_insert)
                    cur.executemany("""
                            INSERT INTO {} (ToolID, PrimaryPurpose)
                            VALUES (%s, %s)
                        """.format(DB_TABLES['tool_primary_purpose']), primary_purposes_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Tools Inserted Successfully'}), 201

@tool_bp.route('/updateTool', methods=['PUT'])
def update_tool():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    tool_data = request.get_json()
    
    name = tool_data.get('name')
    new_name = tool_data.get('newName')
    toolType = tool_data.get('type')
    sync = tool_data.get('sync')
    dateOfRelease = tool_data.get('dateOfRelease')
    primaryPurposes = tool_data.get('primaryPurposes')
    
    if not name:
        return jsonify({'error': 'Tool name must be provided'}), 400
    
    update_fields = []
    update_values = []
    
    if new_name:
        update_fields.append("Name = %s")
        update_values.append(new_name)
    
    if toolType:
        update_fields.append("Type = %s")
        update_values.append(toolType)
    
    if sync:
        update_fields.append("SyncCapability = %s")
        update_values.append(sync)
    
    if dateOfRelease:
        update_fields.append("DateOfRelease = %s")
        update_values.append(dateOfRelease)
    
    if not update_fields and not primaryPurposes:
        return jsonify({'error': 'No fields to update'}), 400
    
    update_values.append(name)
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                if update_fields:
                    cur.execute("""
                        UPDATE {} SET {} WHERE Name = %s
                    """.format(DB_TABLES['tool'], ", ".join(update_fields)), update_values)
                
                if primaryPurposes is not None:
                    cur.execute("""
                        DELETE FROM {} WHERE ToolID = (SELECT ToolID FROM {} WHERE Name = %s)
                    """.format(DB_TABLES['tool_primary_purpose'], DB_TABLES['tool']), (name,))
                    
                    if len(primaryPurposes) > 0:
                        tool_id_query = "SELECT ToolID FROM {} WHERE Name = %s".format(DB_TABLES['tool'])
                        cur.execute(tool_id_query, (name,))
                        tool_id = cur.fetchone()['ToolID']
                        
                        primary_purposes_to_insert = [(tool_id, purpose.strip()) for purpose in primaryPurposes]
                        cur.executemany("""
                            INSERT INTO {} (ToolID, PrimaryPurpose)
                            VALUES (%s, %s)
                        """.format(DB_TABLES['tool_primary_purpose']), primary_purposes_to_insert)
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Tool Updated Successfully'}), 200

@tool_bp.route('/deleteTool', methods=['DELETE'])
def delete_tool():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Tool name must be provided'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    DELETE FROM {} WHERE Name = %s
                """.format(DB_TABLES['tool']), (name,))
                
                if cur.rowcount == 0:
                    return jsonify({'error': 'Tool not found'}), 404
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                return jsonify({'error': True, 'message': 'Error Occurred: ' + str(e)}), 500
    
    return jsonify({'message': 'Tool Deleted Successfully'}), 200