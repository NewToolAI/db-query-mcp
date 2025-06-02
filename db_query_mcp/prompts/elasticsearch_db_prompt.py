query_prompt = '''Generate a single Elasticsearch DSL query to retrieve the required information from the Elasticsearch index.
- Ensuring the generated Elasticsearch DSL is precise, professional, efficient, and executable.
- Strictly generate only read-only queries (search operations) and disallow any write operations (index, update, delete, etc.) on the Elasticsearch cluster.
- Use proper Elasticsearch Query DSL syntax with JSON format.
- Include appropriate filters, aggregations, and sorting as needed.
- Limit the result size appropriately to avoid overwhelming responses.

## Database type: {db_type}

## Database schema:
{db_schema}

Args:
    query (str): The query user input
    statement (dict): The Elasticsearch DSL query to execute
'''

export_prompt = '''Generate a single Elasticsearch DSL query to retrieve the required information from the Elasticsearch index and export it as a JSON file.
- Ensuring the generated Elasticsearch DSL is precise, professional, efficient, and executable.
- Strictly generate only read-only queries (search operations) and disallow any write operations (index, update, delete, etc.) on the Elasticsearch cluster.
- Use proper Elasticsearch Query DSL syntax with JSON format.
- Include appropriate filters, aggregations, and sorting as needed.
- If the user does not specify the path to export the JSON file, export it to the current project directory.
- Use scroll API or search_after for large result sets if necessary.

## Database type: {db_type}

## Database schema:
{db_schema}

Args:
    query (str): The query user input
    statement (dict): The Elasticsearch DSL query to execute
'''
