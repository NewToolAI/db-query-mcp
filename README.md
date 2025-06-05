![image](logo.png)

![Python Version](https://img.shields.io/badge/python-3.10+-aff.svg)
![License](https://img.shields.io/badge/license-Apache%202-dfd.svg)
[![PyPI](https://img.shields.io/pypi/v/db-query-mcp)](https://pypi.org/project/db-query-mcp/)
[![GitHub pull request](https://img.shields.io/badge/PRs-welcome-blue)](https://github.com/Shulin-Zhang/db-query-mcp/pulls)

[ English | [中文](README_ZH.md) ]

# db-query-mcp

## Introduction
db-query-mcp is a mcp tool supporting diverse database querying and exporting, featuring:

- **Multi-DB Support**: Full compatibility with mainstream databases (ElasticSearch, MySQL, PostgreSQL, Oracle, SQLite, etc.)
- **Secure Access**: Default read-only mode for data protection
- **Smart Query**: Natural language to SQL conversion with query optimization
- **Data Export**: CSV / Json export capabilities
- **Roadmap**: Expanding support for MongoDB and GraphDatabase to become full-stack DB query MCP

## Demo
https://github.com/user-attachments/assets/60771cda-8b52-41bd-90e3-523c836f6366

## Changelog

- 2025-06-02: Added support for ElasticSearch database queries

## Installation

```bash
pip install db-query-mcp
```

ElasticSearch:
```bash
pip install db-query-mcp[elasticsearch]
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

**For some clients, only one db-query-mcp server can be enabled at a time.**

```json
{
  "mcpServers": {
      "sqlite_db_mcp": {
        "command": "db-query-mcp",
        "args": [
          "--db",
          "sqlite",
          "--uri", 
          "sqlite:///sqlite_company.db"
        ]
      }
  }
}
```

```json
{
  "mcpServers": {
      "es_db_mcp": {
        "command": "db-query-mcp",
        "args": [
          "--db",
          "elasticsearch",
          "--uri", 
          "https://user:password@localhost:9200?index=test_data_index&ca_certs=/home/user/http_ca.crt"
        ]
      }
  }
}
```
