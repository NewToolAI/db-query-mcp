![image](logo.png)

![Python Version](https://img.shields.io/badge/python-3.10+-aff.svg)
![License](https://img.shields.io/badge/license-Apache%202-dfd.svg)
[![PyPI](https://img.shields.io/pypi/v/db-query-mcp)](https://pypi.org/project/db-query-mcp/)
[![GitHub pull request](https://img.shields.io/badge/PRs-welcome-blue)](https://github.com/Shulin-Zhang/db-query-mcp/pulls)

\[ [中文](README_ZH.md) | English \]

# db-query-mcp

## Introduction
db-query-mcp is an MCP tool that enables data querying and export operations across diverse databases, featuring:​

- **Multi-Database Support**: Full compatibility with mainstream relational databases (MySQL, PostgreSQL, Oracle, SQLite, etc.)
- **Secure Access**: Default read-only mode connection ensures data safety
- **Smart Query**: Provides efficient SQL generation and execution capabilities
- **Data Export**: Supports query result export functionality
- Future versions will expand support for Elasticsearch, MongoDB, and graph databases, aiming to become a full-stack database query solution.

## Demo
https://github.com/user-attachments/assets/51d0e890-27b2-411d-b5c3-e748599a9543

## Installation

```bash
pip install db-query-mcp
```

Install from GitHub:
```bash
pip install git+https://github.com/NewToolAI/db-query-mcp
```

**MySQL requires additional dependencies:**
```bash
pip install pymysql
```

**PostgreSQL requires additional dependencies:**
```bash
pip install psycopg2-binary
```

**For other databases, install their respective connection packages:**

| Database    | Connection Package       | Example Connection String |
|-------------|--------------------------|---------------------------|
| **SQLite**  | Built-in Python          | `sqlite:///example.db`    |
| **MySQL**   | `pymysql` or `mysql-connector-python` | `mysql+pymysql://user:password@localhost/dbname` |
| **PostgreSQL** | `psycopg2` or `psycopg2-binary` | `postgresql://user:password@localhost:5432/dbname` |
| **Oracle**  | `cx_Oracle`              | `oracle+cx_oracle://user:password@hostname:1521/sidname` |
| **SQL Server** | `pyodbc` or `pymssql` | `mssql+pyodbc://user:password@hostname/dbname` |

## Configuration

```json
{
  "mcpServers": {
    "db_query_mcp": {
      "command": "db-query-mcp",
      "args": [
        "--db",
        "mysql+pymysql://user:password@host:port/database"
      ]
    }
  }
}
```
