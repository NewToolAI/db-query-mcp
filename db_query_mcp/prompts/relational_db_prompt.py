query_prompt = '''Generate a single SQL query to retrieve the required information from the database.
- Ensuring the generated SQL is precise, professional, efficient, and executable. 
- Strictly generate only read-only SQL statements (SELECT queries) and disallow any write operations (INSERT, UPDATE, DELETE, etc.) on the database.
- Ensure the field names are enclosed in double quotes ("") to avoid SQL syntax errors.

## Database type: {db_type}

{db_schema}
'''

export_prompt = '''Generate a single SQL query to retrieve the required information from the database and export it as a CSV file. 
- Ensuring the generated SQL is precise, professional, efficient, and executable. 
- Strictly generate only read-only SQL statements (SELECT queries) and disallow any write operations (INSERT, UPDATE, DELETE, etc.) on the database.
- Ensure the field names are enclosed in double quotes ("") to avoid SQL syntax errors.
- If the user does not specify the path to export the CSV file, export it to the current project directory.

## Database type: {db_type}

{db_schema}
'''
