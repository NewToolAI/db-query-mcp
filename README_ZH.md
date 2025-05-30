![image](logo.png)

![Python Version](https://img.shields.io/badge/python-3.10+-aff.svg)
![License](https://img.shields.io/badge/license-Apache%202-dfd.svg)
[![PyPI](https://img.shields.io/pypi/v/db-query-mcp)](https://pypi.org/project/db-query-mcp/)
[![GitHub pull request](https://img.shields.io/badge/PRs-welcome-blue)](https://github.com/Shulin-Zhang/db-query-mcp/pulls)

\[ 中文 | [English](README.md) \]

# db-query-mcp

## 简介
db-query-mcp 是一个支持多种数据库查询和导出的 MCP 工具，具有以下核心特性：

- ​多数据库支持​：全面兼容主流关系型数据库（MySQL、PostgreSQL、Oracle、SQLite等）；
- 安全访问​：默认以只读模式连接数据库，保障数据安全；
- 智能查询​：提供高效的SQL生成与执行能力；
- ​数据导出​：支持查询结果导出功能；
- 未来版本规划将扩展对 Elasticsearch、MongoDB 以及图数据库的支持，致力于成为全栈式数据库查询解决方案。

## 演示
https://github.com/user-attachments/assets/51d0e890-27b2-411d-b5c3-e748599a9543

## 安装

```bash
pip install db-query-mcp
```

源码安装：
```bash
pip install git+https://github.com/NewToolAI/db-query-mcp
```

mysql需要额外安装依赖:
```bash
pip install pymysql
```

postgredb需要额外安装依赖:
```bash
pip install psycopg2-binary
```

**对于其他数据库，需要额外安装相应的数据库连接包。**

| Database    | Connection Package       | Example Connection String |
|-------------|--------------------------|--------------------------|
| **SQLite**  | (Python 内置) | `sqlite:///example.db` |
| **MySQL**   | `pymysql` 或 `mysql-connector-python` | `mysql+pymysql://user:password@localhost/dbname` |
| **PostgreSQL** | `psycopg2、psycopg2-binary` | `postgresql://user:password@localhost:5432/dbname` |
| **Oracle**  | `cx_Oracle` | `oracle+cx_oracle://user:password@hostname:1521/sidname` |
| **SQL Server** | `pyodbc` 或 `pymssql` | `mssql+pyodbc://user:password@hostname/dbname`    |

## 配置

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
