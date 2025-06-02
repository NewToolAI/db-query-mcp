from db_query_mcp.db_adapters.base_adapter import BaseAdapter


relational_dbs = [
    'sqlite',      # SQLite
    'postgresql',  # PostgreSQL (如 psycopg2)
    'mysql',       # MySQL (如 pymysql)
    'oracle',      # Oracle (如 cx_Oracle)
    'mssql',       # Microsoft SQL Server (如 pyodbc)
    'firebird',    # Firebird
    'sybase',      # Sybase
    'db2',         # IBM DB2
    'informix',    # IBM Informix
]



def create_db(db: str, uri: str) -> BaseAdapter:
    db_uri, args = parse_uri(uri)

    if db in relational_dbs:
        from db_query_mcp.db_adapters.relational_db_adapter import RelationalDBAdapter

        return RelationalDBAdapter(db_uri, **args)
    elif db == 'elasticsearch':
        from db_query_mcp.db_adapters.elasticsearch_db_adapter import ElasticsearchDBAdapter
            
        return ElasticsearchDBAdapter(db_uri, **args)
    else:
        raise ValueError(f'Unsupported database type: {db}')


def create_sql_prompt(db_type: str, db_schema: str) -> str:
    if db_type in relational_dbs:
        from db_query_mcp.prompts import relational_db_prompt

        query_prompt = relational_db_prompt.query_prompt.format(db_type=db_type, db_schema=db_schema)
        export_prompt = relational_db_prompt.export_prompt.format(db_type=db_type, db_schema=db_schema)
        return query_prompt, export_prompt

    elif db_type == 'elasticsearch':
        from db_query_mcp.prompts import elasticsearch_db_prompt

        query_prompt = elasticsearch_db_prompt.query_prompt.format(db_type=db_type, db_schema=db_schema)
        export_prompt = elasticsearch_db_prompt.export_prompt.format(db_type=db_type, db_schema=db_schema)
        return query_prompt, export_prompt

    else:
        raise ValueError(f'Unsupported database type: {db_type}')


def parse_uri(uri: str) -> str:
    if uri.count('?') == 1:
        uri, args = uri.split('?')
        args = args.split('&')
        args = {k.strip(): v.strip() for k, v in [arg.split('=') for arg in args]}
    elif uri.count('?') == 0:
        args = {}
    else:
        raise ValueError(f'Invalid URI: {uri}')

    return uri.strip(), args
