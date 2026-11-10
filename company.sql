CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT NOT NULL);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept_id INTEGER REFERENCES departments(dept_id), salary REAL, hire_date TEXT);
INSERT INTO departments VALUES (1,'Sales'),(2,'Engineering'),(3,'HR'),(4,'Finance');
WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i+1 FROM n WHERE i<300)
INSERT INTO employees SELECT i, 'Employee '||i, (i%4)+1, 30000+((i*7919)%70000), date('2018-01-01','+'||((i*37)%2500)||' days') FROM n;
