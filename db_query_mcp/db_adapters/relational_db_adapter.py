from typing import Dict
from pathlib import Path

from sqlalchemy import inspect, create_engine, text, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine


from db_query_mcp.db_adapters.base_adapter import BaseAdapter


__all__ = ['SqlalchemyAdapter']


supported_dbs = [
    'sqlite',      # SQLite（内置支持，无需额外驱动）
    'postgresql',  # PostgreSQL (如 psycopg2)
    'mysql',       # MySQL (如 pymysql)
    'oracle',      # Oracle (如 cx_Oracle)
    'mssql',       # Microsoft SQL Server (如 pyodbc)
    'firebird',    # Firebird
    'sybase',      # Sybase
    'db2',         # IBM DB2
    'informix',    # IBM Informix
]


class SqlalchemyAdapter(BaseAdapter):
    
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        self.engine = create_engine(db_uri)

    def query(self, sql: str) -> Dict:
        self._check_sql(sql)

        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = list(result.keys())  
            data = result.fetchall()

            return self._format_query_result_to_markdown(columns, data)

    def export(self, sql: str, output: str):
        sql = self._check_sql(sql)

        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = list(result.keys())
            data = result.fetchall()

            output = Path(output)

            if output.is_dir():
                path = output / 'export.csv'
                if path.exists():
                    raise FileExistsError(f'File {output} already exists.')
            elif output.exists():
                raise FileExistsError(f'File {output} already exists.')
            else:
                path = output

            self._export_to_file(path, columns, data)
            return f'Successfully exported the data to {path.resolve()}'

    def get_db_type(self) -> str:
        try:
            db_type = self.db_uri.split(':')[0].lower()
            if db_type not in supported_dbs:
                raise ValueError(f'Unsupported database type: {db_type}')
        except Exception:
            raise ValueError(f'Your db uri is not valid: {self.db_uri}')

        return db_type

    def get_db_schema(self, include_foreign_keys: bool = True) -> Dict[str, Dict]:
        schema = {}
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
        
            for table_name in tables:
                table_info = {
                    'columns': [],
                    'primary_key': [],
                    'foreign_keys': []
                }
            
                for column in inspector.get_columns(table_name):
                    table_info['columns'].append({
                        'name': column['name'],
                        'type': column['type'],
                        'nullable': column['nullable'],
                        'default': column['default']
                    })
            
                pk_info = inspector.get_pk_constraint(table_name)
                table_info['primary_key'] = pk_info.get('constrained_columns', [])
            
                if include_foreign_keys:
                    for fk in inspector.get_foreign_keys(table_name):
                        table_info['foreign_keys'].append({
                            'constrained_columns': fk['constrained_columns'],
                            'referred_table': fk['referred_table'],
                            'referred_columns': fk['referred_columns']
                        })
            
                schema[table_name] = table_info
                schema = self._format_schema_to_markdown(schema)

            return schema
        
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f'Failed to obtain the database schema: {str(e)}')

    @event.listens_for(Engine, "before_execute")
    def before_execute(conn, clauseelement, multiparams, params):
        if clauseelement.is_dml:
            raise Exception("Only support query operations.")

    def _check_sql(self, sql: str) -> bool:
        sql = sql.strip()

        if 'SELECT ' not in sql.upper():
            raise ValueError('Only support query operations.') 

        for action in ['INSERT ', 'UPDATE ', 'DELETE ', 'DROP ', 'CREATE ', 'ALTER ']:
            if action in sql.upper():
                raise ValueError(f'Only support query operations.')

        return  sql

    def _export_to_file(self, output: str, columns: list, data: list):
        with open(output, 'w', encoding='utf-8') as f:
            columns = ', '.join(columns)
            f.write(f'{columns}\n')

            for row in data:
                row = ', '.join([f'"{value}"' if "'" in str(value) else str(value) for value in row])
                f.write(f'{row}\n')

    def _format_schema_to_markdown(self, schema: Dict[str, Dict]) -> str:
        markdown_output = []
        markdown_output.append('## Database Schema\n')
    
        for table_name, table_info in schema.items():
            # Table header
            markdown_output.append(f'### Table name: `{table_name}`\n')
        
            # Columns table
            if table_info.get('columns'):
                markdown_output.append('### Table columns\n')
                markdown_output.append('| Column Name | Data Type | Nullable | Default Value | Primary Key |')
                markdown_output.append('|---|---|---|---|---|')
            
                primary_keys = table_info.get('primary_key', [])
            
                for column in table_info['columns']:
                    name = column['name']
                    data_type = str(column['type'])
                    nullable = '✓' if column['nullable'] else '✗'
                    default = str(column['default']) if column['default'] is not None else '-'
                    is_pk = '✓' if name in primary_keys else '✗'
                
                    markdown_output.append(f'| {name} | {data_type} | {nullable} | {default} | {is_pk} |')
            
                markdown_output.append('')
        
            # Primary Keys section
            if table_info.get('primary_key'):
                markdown_output.append('#### Primary Keys\n')
                pk_list = ', '.join([f'`{pk}`' for pk in table_info['primary_key']])
                markdown_output.append(f'**Primary Key(s):** {pk_list}\n')
        
            # Foreign Keys section
            if table_info.get('foreign_keys'):
                markdown_output.append('#### Foreign Keys\n')
                markdown_output.append('| Local Column(s) | Referenced Table | Referenced Column(s) |')
                markdown_output.append('|---|---|---|')
            
                for fk in table_info['foreign_keys']:
                    local_cols = ', '.join([f'`{col}`' for col in fk['constrained_columns']])
                    ref_table = f'`{fk["referred_table"]}`'
                    ref_cols = ', '.join([f'`{col}`' for col in fk['referred_columns']])
                
                    markdown_output.append(f'| {local_cols} | {ref_table} | {ref_cols} |')
            
                markdown_output.append('')
        
            markdown_output.append('---\n')
    
        return '\n'.join(markdown_output)

    def _format_query_result_to_markdown(self, columns: list, data: list) -> str:
        if not columns:
            return 'No column names available'
            
        if not data:
            return f'Query result is empty\n\n**Column names:** {", ".join(columns)}'
        
        markdown_lines = []
        
        header = '| ' + ' | '.join(columns) + ' |'
        markdown_lines.append(header)
        
        separator = '|' + '|'.join([' --- ' for _ in columns]) + '|'
        markdown_lines.append(separator)
        
        for row in data:
            formatted_row = []
            for value in row:
                if value is None:
                    formatted_row.append('NULL')
                else:
                    cell_value = str(value).replace('|', '\\|')  # 转义管道符
                    formatted_row.append(cell_value)
            
            row_str = '| ' + ' | '.join(formatted_row) + ' |'
            markdown_lines.append(row_str)
        
        result_summary = f'\n**Query result summary:** {len(data)} rows, {len(columns)} columns'
        markdown_lines.append(result_summary)
        
        result = '\n'.join(markdown_lines)
        return result
