import sqlite3

conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

# ----------------------------
# Create tables
# ----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    cost_center TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    job_title TEXT,
    department_id INTEGER,
    manager_employee_id TEXT,
    hire_date TEXT,
    employment_type TEXT,
    status TEXT,
    base_salary INTEGER,
    location TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
)
""")

# ----------------------------
# Insert departments
# ----------------------------

departments = [
    (1, "Engineering", "ENG-001"),
    (2, "Finance", "FIN-002"),
    (3, "Human Resources", "HR-003"),
]

cursor.executemany(
    "INSERT OR IGNORE INTO departments VALUES (?, ?, ?)",
    departments
)

# ----------------------------
# Insert employees (10 rows)
# ----------------------------

employees = [
    ("EMP-1001", "Amit", "Sharma", "amit.sharma@company.com", "Senior Engineer", 1, None, "2020-06-15", "Full-time", "Active", 2200000, "Bangalore"),
    ("EMP-1002", "Neha", "Verma", "neha.verma@company.com", "Engineering Manager", 1, None, "2018-03-10", "Full-time", "Active", 3000000, "Bangalore"),
    ("EMP-1003", "Rahul", "Mehta", "rahul.mehta@company.com", "Backend Engineer", 1, "EMP-1002", "2022-01-20", "Full-time", "Active", 1800000, "Bangalore"),

    ("EMP-1004", "Priya", "Singh", "priya.singh@company.com", "Finance Manager", 2, None, "2019-09-01", "Full-time", "Active", 2800000, "Delhi"),
    ("EMP-1005", "Arjun", "Kapoor", "arjun.kapoor@company.com", "Financial Analyst", 2, "EMP-1004", "2021-11-05", "Full-time", "Active", 1600000, "Delhi"),
    ("EMP-1006", "Kavya", "Nair", "kavya.nair@company.com", "Accounts Executive", 2, "EMP-1004", "2023-02-18", "Full-time", "Active", 1200000, "Delhi"),

    ("EMP-1007", "James", "Brown", "james.brown@company.com", "HR Lead", 3, None, "2017-05-12", "Full-time", "Active", 2500000, "London"),
    ("EMP-1008", "Emily", "Clark", "emily.clark@company.com", "HR Business Partner", 3, "EMP-1007", "2020-08-25", "Full-time", "On Leave", 1900000, "London"),
    ("EMP-1009", "Oliver", "Wilson", "oliver.wilson@company.com", "Recruiter", 3, "EMP-1007", "2022-06-30", "Contractor", "Active", 1400000, "London"),

    ("EMP-1010", "Daniel", "Miller", "daniel.miller@company.com", "Site Reliability Engineer", 1, "EMP-1002", "2021-10-14", "Full-time", "Active", 2600000, "London"),
]

cursor.executemany("""
INSERT INTO employees (
    employee_id, first_name, last_name, email,
    job_title, department_id, manager_employee_id,
    hire_date, employment_type, status,
    base_salary, location
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", employees)

conn.commit()
conn.close()

print("✅ Employee database initialized with 10 real-world records.")
