from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Employee MCP Server")

DB_PATH = "employees.db"


# -----------------------------
# Database helper
# -----------------------------
def get_db():
    return sqlite3.connect(DB_PATH)


# -----------------------------
# MCP Tool Input Schemas
# -----------------------------

class EmployeeByNameInput(BaseModel):
    first_name: str


class EmployeesByLocationInput(BaseModel):
    location: str


class EmployeesByDepartmentInput(BaseModel):
    department: str


class DirectReportsInput(BaseModel):
    manager_employee_id: str


# -----------------------------
# MCP Tools
# -----------------------------

@app.post("/tools/get_employee_by_name")
def get_employee_by_name(data: EmployeeByNameInput):
    """
    Get employee details using first name
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT employee_id, first_name, last_name, job_title,
               base_salary, location, status
        FROM employees
        WHERE first_name = ?
    """, (data.first_name,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Employee not found"}

    return {
        "employee_id": row[0],
        "name": f"{row[1]} {row[2]}",
        "job_title": row[3],
        "base_salary": row[4],
        "location": row[5],
        "status": row[6],
    }


@app.post("/tools/get_employees_by_location")
def get_employees_by_location(data: EmployeesByLocationInput):
    """
    List all employees in a given location
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT first_name, last_name, job_title
        FROM employees
        WHERE location = ?
    """, (data.location,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "name": f"{r[0]} {r[1]}",
            "job_title": r[2]
        }
        for r in rows
    ]


@app.post("/tools/get_direct_reports")
def get_direct_reports(data: DirectReportsInput):
    """
    Get employees reporting to a specific manager
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT first_name, last_name, job_title
        FROM employees
        WHERE manager_employee_id = ?
    """, (data.manager_employee_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "name": f"{r[0]} {r[1]}",
            "job_title": r[2]
        }
        for r in rows
    ]


# -----------------------------
# MCP Tool Registry
# -----------------------------

@app.get("/mcp/tools")
def list_tools():
    """
    Tool discovery endpoint (core MCP concept)
    """
    return [
        {
            "name": "get_employee_by_name",
            "description": "Get employee details by first name",
            "endpoint": "/tools/get_employee_by_name",
            "input_schema": {
                "first_name": "string"
            }
        },
        {
            "name": "get_employees_by_location",
            "description": "List all employees in a specific location",
            "endpoint": "/tools/get_employees_by_location",
            "input_schema": {
                "location": "string"
            }
        },
        {
            "name": "get_direct_reports",
            "description": "Get employees reporting to a manager",
            "endpoint": "/tools/get_direct_reports",
            "input_schema": {
                "manager_employee_id": "string"
            }
        }
    ]
