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


def create_db(db_uri: str) -> BaseAdapter:
    db_type = db_uri.split(':')[0].lower()

    if db_type in relational_dbs:
        from db_query_mcp.db_adapters.relational_db_adapter import RelationalDBAdapter

        return RelationalDBAdapter(db_uri)
    else:
        raise ValueError(f'Unsupported database type: {db_type}')


def create_sql_prompt(db_type: str, db_schema: str) -> str:
    if db_type in relational_dbs:
        from db_query_mcp.prompts import relational_db_prompt

        query_prompt = relational_db_prompt.query_prompt.format(db_type=db_type, db_schema=db_schema)
        export_prompt = relational_db_prompt.export_prompt.format(db_type=db_type, db_schema=db_schema)
        return query_prompt, export_prompt
    else:
        raise ValueError(f'Unsupported database type: {db_type}')
