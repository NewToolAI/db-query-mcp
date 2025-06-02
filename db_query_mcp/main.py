from typing import Union
from argparse import ArgumentParser
from mcp.server.fastmcp import FastMCP

from db_query_mcp import factory


parser = ArgumentParser()
parser.add_argument('--db', type=str, required=True)
parser.add_argument('--uri', type=str, required=True)
args = parser.parse_args()


db = factory.create_db(args.db, args.uri)
query_prompt, export_prompt = factory.create_sql_prompt(db.get_db_type(), db.get_db_schema())

mcp = FastMCP('db_query_mcp')


@mcp.tool(description=query_prompt)
def query_database(query: str, statement: Union[str, dict]) -> str:
    f'''Query the database
    Args:
        query: The query user input.
        statement: The database statement to execute.
    '''
    result = db.query(statement)
    return result 


@mcp.tool(description=export_prompt)
def export_database(query: str, statement: Union[str, dict], path: str) -> str:
    f'''Query the database and export the data to a csv file
    Args:
        query: The query user input.
        statement: The database statement to execute.
        path: The file path to export the data.
    '''
    result = db.export(statement, path)
    return result


def run():
    mcp.run(transport='stdio')


if __name__ == '__main__':
    run()
